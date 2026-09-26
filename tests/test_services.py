"""Tests for service-layer classes.

Covers:
  - AuthService: login, register_student, register_admin, duplicate handling
  - FileService: CSV/JSON/text import/export, missing files, empty data
  - ReportService: DataFrame generation, chart export, daily quote fallback
"""

import json
import os
import pytest

from src.exceptions.custom_exceptions import (
    InvalidCredentialsError,
    DuplicateUsernameError,
    FileOperationError,
    ReportGenerationError,
)
from unittest.mock import Mock, patch

from src.services.external_service import (
    ExternalTimeService,
    ExternalServiceError,
)


# ======================================================================= #
# AuthService                                                              #
# ======================================================================= #

class TestAuthService:

    def test_register_student(self, auth_service, user_repo):
        student = auth_service.register_student("newstu", "pw12345", "New Student", "ns@ibsu.edu")
        assert student.username == "newstu"
        assert student.role == "student"

    def test_register_admin(self, auth_service, user_repo):
        admin = auth_service.register_admin("newadm", "pw12345", "New Admin")
        assert admin.username == "newadm"
        assert admin.role == "admin"

    def test_register_duplicate_raises(self, auth_service):
        auth_service.register_student("dup", "pw12345", "Dup")
        with pytest.raises(DuplicateUsernameError):
            auth_service.register_student("dup", "pw12345", "Dup2")

    def test_login_success(self, auth_service):
        auth_service.register_student("logme", "pw12345", "Log Me")
        user = auth_service.login("logme", "pw12345")
        assert user.username == "logme"

    def test_login_wrong_password(self, auth_service):
        auth_service.register_student("wrongpw", "pw12345", "Wrong")
        with pytest.raises(InvalidCredentialsError):
            auth_service.login("wrongpw", "nope")

    def test_login_unknown_user(self, auth_service):
        with pytest.raises(InvalidCredentialsError):
            auth_service.login("ghost", "pw12345")


# ======================================================================= #
# FileService                                                              #
# ======================================================================= #

class TestFileServiceCSV:

    def test_export_and_import_csv(self, file_service, tmp_path):
        data = [
            {"name": "Pasta", "price": 5.5, "stock": 20},
            {"name": "Salad", "price": 4.0, "stock": 30},
        ]
        path = str(tmp_path / "menu.csv")
        file_service.export_csv(path, data, ["name", "price", "stock"])
        assert os.path.isfile(path)

        rows = file_service.import_csv(path)
        assert len(rows) == 2
        assert rows[0]["name"] == "Pasta"

    def test_export_csv_empty_data(self, file_service, tmp_path):
        path = str(tmp_path / "empty.csv")
        # Should not write a file and should not raise
        file_service.export_csv(path, [])

    def test_import_csv_missing_file(self, file_service):
        with pytest.raises(FileOperationError):
            file_service.import_csv("/nonexistent/path/file.csv")


class TestFileServiceJSON:

    def test_export_and_import_json(self, file_service, tmp_path):
        data = {"categories": [{"id": 1, "name": "Main"}, {"id": 2, "name": "Drink"}]}
        path = str(tmp_path / "cats.json")
        file_service.export_json(path, data)
        assert os.path.isfile(path)

        result = file_service.import_json(path)
        assert len(result["categories"]) == 2

    def test_import_json_invalid_file(self, file_service, tmp_path):
        bad_path = str(tmp_path / "bad.json")
        with open(bad_path, "w") as f:
            f.write("{invalid json")
        with pytest.raises(FileOperationError):
            file_service.import_json(bad_path)

    def test_import_json_missing_file(self, file_service):
        with pytest.raises(FileOperationError):
            file_service.import_json("/nonexistent/path/file.json")


class TestFileServiceText:

    def test_export_text_report(self, file_service, tmp_path):
        path = str(tmp_path / "report.txt")
        file_service.export_text_report(path, "Hello report")
        assert os.path.isfile(path)
        with open(path) as f:
            assert f.read() == "Hello report"

    def test_append_text_report(self, file_service, tmp_path):
        path = str(tmp_path / "log.txt")
        file_service.append_text_report(path, "line 1")
        file_service.append_text_report(path, "line 2")
        with open(path) as f:
            content = f.read()
        assert "line 1" in content
        assert "line 2" in content

    def test_get_export_path(self, file_service):
        p = file_service.get_export_path("sales.csv")
        assert "exports" in p
        assert p.endswith(".csv")


# ======================================================================= #
# ReportService                                                            #
# ======================================================================= #

class TestReportService:

    def test_daily_sales_dataframe_empty(self, report_service):
        df = report_service.get_daily_sales_dataframe("2020-01-01")
        assert df.empty
        assert "order_id" in df.columns

    def test_popular_items_dataframe_empty(self, report_service):
        df = report_service.get_popular_items_dataframe()
        assert df.empty

    def test_category_sales_dataframe_empty(self, report_service):
        df = report_service.get_category_sales_dataframe()
        assert df.empty

    def test_daily_sales_bar_empty_returns_empty_string(self, report_service):
        path = report_service.plot_daily_sales_bar("2020-01-01")
        assert path == ""

    def test_popular_items_pie_empty_returns_empty_string(self, report_service):
        path = report_service.plot_popular_items_pie()
        assert path == ""

    def test_category_sales_bar_empty_returns_empty_string(self, report_service):
        path = report_service.plot_category_sales_bar()
        assert path == ""

    def test_export_full_report_empty(self, report_service):
        paths = report_service.export_full_report("2020-01-01")
        assert "text" in paths
        assert "csv" in paths
        assert "json" in paths
        # Verify text file created
        assert os.path.isfile(paths["text"])

    def test_report_with_data(self, report_service, order_repo, user_repo, food_repo, category_repo, order_status_repo):
        student = user_repo.create_student("rpt_stu", "pw12345", "Rpt Stu")
        cat = category_repo.create("RptCat", "Category")
        item = food_repo.create(cat.category_id, "RptItem", "Desc", 4.0, 20)
        pending = order_status_repo.get_by_name("received")
        items = [{"food_item_id": item.food_item_id, "name": item.name, "price": item.price, "quantity": 3}]
        order_id = order_repo.create(student.user_id, pending["status_id"], items)

        df = report_service.get_popular_items_dataframe()
        assert not df.empty
        assert df.iloc[0]["total_qty"] == 3

        df2 = report_service.get_category_sales_dataframe()
        assert not df2.empty
        
        
class TestExternalTimeService:

    @patch("src.services.external_service.requests.get")
    def test_external_time_service_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "timezone": "Pacific/Port_Moresby",
            "datetime": "2026-09-22T14:30:00+10:00",
            "utc_offset": "+10:00",
        }
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        service = ExternalTimeService()
        result = service.get_current_time()

        assert result["available"] is True
        assert result["status_code"] == 200
        assert result["timezone"] == "Pacific/Port_Moresby"
        assert result["utc_offset"] == "+10:00"

        mock_get.assert_called_once()

    @patch("src.services.external_service.requests.get")
    def test_external_time_service_timeout(self, mock_get):
        import requests

        mock_get.side_effect = requests.Timeout()

        service = ExternalTimeService()

        with pytest.raises(ExternalServiceError):
            service.get_current_time()

    @patch("src.services.external_service.requests.get")
    def test_external_time_service_http_error(self, mock_get):
        import requests

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "503 Service Unavailable"
        )

        mock_get.return_value = mock_response

        service = ExternalTimeService()

        with pytest.raises(ExternalServiceError):
            service.get_current_time()

    @patch("src.services.external_service.requests.get")
    def test_external_time_service_invalid_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "unexpected": "data"
        }

        mock_get.return_value = mock_response

        service = ExternalTimeService()

        with pytest.raises(ExternalServiceError):
            service.get_current_time()