"""ReportService — data analysis with pandas, charts with matplotlib,
"""

import logging
import os
from datetime import datetime
from typing import Any

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless environments
import matplotlib.pyplot as plt
import pandas as pd

from ..repositories.order_repository import OrderRepository
from ..repositories.food_item_repository import FoodItemRepository
from ..repositories.category_repository import CategoryRepository
from ..services.file_service import FileService
from ..exceptions.custom_exceptions import ReportGenerationError

logger = logging.getLogger("ibsu_lunch")


class ReportService:
    """Generates analytical reports and charts."""

    def __init__(
        self,
        order_repo: OrderRepository,
        food_item_repo: FoodItemRepository,
        category_repo: CategoryRepository,
        file_service: FileService,
    ) -> None:
        self._order_repo = order_repo
        self._food_repo = food_item_repo
        self._category_repo = category_repo
        self._file_svc = file_service

    # ------------------------------------------------------------------ #
    # Pandas-powered reports                                               #
    # ------------------------------------------------------------------ #

    def get_daily_sales_dataframe(self, date: str | None = None) -> pd.DataFrame:
        """Return a DataFrame of daily completed-order sales.

        Args:
            date: Optional ISO date string (YYYY-MM-DD).  If *None*, today.

        Returns:
            DataFrame with columns: order_id, student_name, total_amount, status.
        """
        try:
            target = date or datetime.now().strftime("%Y-%m-%d")
            rows = self._order_repo.get_daily_sales(target)
            df = pd.DataFrame(rows, columns=["order_id", "student_name", "total_amount", "status"]) if rows else pd.DataFrame(columns=["order_id", "student_name", "total_amount", "status"])
            logger.info("Daily sales DataFrame built for %s (%d rows).", target, len(df))
            return df
        except Exception as exc:
            raise ReportGenerationError("daily_sales", str(exc)) from exc

    def get_popular_items_dataframe(self, limit: int = 10) -> pd.DataFrame:
        """Return a DataFrame of the most-ordered food items."""
        try:
            rows = self._order_repo.get_popular_items(limit)
            df = pd.DataFrame(rows, columns=["food_item_id", "name", "total_qty", "revenue"]) if rows else pd.DataFrame(columns=["food_item_id", "name", "total_qty", "revenue"])
            logger.info("Popular items DataFrame built (%d rows).", len(df))
            return df
        except Exception as exc:
            raise ReportGenerationError("popular_items", str(exc)) from exc

    def get_category_sales_dataframe(self) -> pd.DataFrame:
        """Return a DataFrame of sales grouped by category."""
        try:
            rows = self._order_repo.get_category_sales()
            df = pd.DataFrame(rows, columns=["category_id", "category_name", "total_revenue", "order_count"]) if rows else pd.DataFrame(columns=["category_id", "category_name", "total_revenue", "order_count"])
            logger.info("Category sales DataFrame built (%d rows).", len(df))
            return df
        except Exception as exc:
            raise ReportGenerationError("category_sales", str(exc)) from exc

    # ------------------------------------------------------------------ #
    # Matplotlib charts                                                    #
    # ------------------------------------------------------------------ #

    def plot_daily_sales_bar(self, date: str | None = None) -> str:
        """Save a bar chart of daily sales totals per order and return the path."""
        try:
            df = self.get_daily_sales_dataframe(date)
            if df.empty:
                logger.warning("No sales data to plot for %s.", date)
                return ""
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df["order_id"].astype(str), df["total_amount"], color="#4CAF50")
            ax.set_xlabel("Order ID")
            ax.set_ylabel("Total Amount (K)")
            ax.set_title(f"Daily Sales — {date or 'Today'}")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            path = self._file_svc.get_export_path("daily_sales_bar.png")
            fig.savefig(path)
            plt.close(fig)
            logger.info("Daily sales bar chart saved: %s", path)
            return path
        except Exception as exc:
            raise ReportGenerationError("daily_sales_chart", str(exc)) from exc

    def plot_popular_items_pie(self, limit: int = 10) -> str:
        """Save a pie chart of popular items and return the path."""
        try:
            df = self.get_popular_items_dataframe(limit)
            if df.empty:
                logger.warning("No popular-items data to plot.")
                return ""
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(df["total_qty"], labels=df["name"], autopct="%1.1f%%", startangle=140)
            ax.set_title("Most Popular Menu Items")
            plt.tight_layout()
            path = self._file_svc.get_export_path("popular_items_pie.png")
            fig.savefig(path)
            plt.close(fig)
            logger.info("Popular items pie chart saved: %s", path)
            return path
        except Exception as exc:
            raise ReportGenerationError("popular_items_chart", str(exc)) from exc

    def plot_category_sales_bar(self) -> str:
        """Save a bar chart of revenue by category and return the path."""
        try:
            df = self.get_category_sales_dataframe()
            if df.empty:
                logger.warning("No category sales data to plot.")
                return ""
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(df["category_name"], df["total_revenue"], color="#2196F3")
            ax.set_xlabel("Category")
            ax.set_ylabel("Revenue (K)")
            ax.set_title("Revenue by Category")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            path = self._file_svc.get_export_path("category_sales_bar.png")
            fig.savefig(path)
            plt.close(fig)
            logger.info("Category sales chart saved: %s", path)
            return path
        except Exception as exc:
            raise ReportGenerationError("category_sales_chart", str(exc)) from exc

    # ------------------------------------------------------------------ #
    # Composite text / CSV / JSON report export                            #
    # ------------------------------------------------------------------ #

    def export_full_report(self, date: str | None = None) -> dict[str, str]:
        """Export a full report bundle (text, CSV, JSON) for a given date.

        Returns:
            Dict mapping format name → file path.
        """
        try:
            sales_df = self.get_daily_sales_dataframe(date)
            popular_df = self.get_popular_items_dataframe()
            cat_df = self.get_category_sales_dataframe()
            target = date or datetime.now().strftime("%Y-%m-%d")

            paths: dict[str, str] = {}

            # Plain-text summary
            text_lines = [
                f"=== IBSU Lunch Ordering System — Daily Report ===",
                f"Date: {target}",
                "",
                "--- Completed Orders ---",
            ]
            if not sales_df.empty:
                for _, row in sales_df.iterrows():
                    text_lines.append(f"  Order #{row['order_id']}: {row['student_name']} — K{row['total_amount']:.2f} ({row['status']})")
                text_lines.append(f"  Total revenue: K{sales_df['total_amount'].sum():.2f}")
            else:
                text_lines.append("  No completed orders.")

            text_lines.append("")
            text_lines.append("--- Popular Items ---")
            if not popular_df.empty:
                for _, row in popular_df.iterrows():
                    text_lines.append(f"  {row['name']}: {row['total_qty']} sold (K{row['revenue']:.2f})")
            else:
                text_lines.append("  No data.")

            text_lines.append("")
            text_lines.append("--- Category Revenue ---")
            if not cat_df.empty:
                for _, row in cat_df.iterrows():
                    text_lines.append(f"  {row['category_name']}: K{row['total_revenue']:.2f} ({row['order_count']} orders)")
            else:
                text_lines.append("  No data.")

            text_content = "\n".join(text_lines)
            txt_path = self._file_svc.get_export_path(f"report_{target}.txt")
            self._file_svc.export_text_report(txt_path, text_content)
            paths["text"] = txt_path

            # CSV export
            csv_path = self._file_svc.get_export_path(f"sales_{target}.csv")
            self._file_svc.export_csv(csv_path, sales_df.to_dict("records"))
            paths["csv"] = csv_path

            # JSON export
            json_data = {
                "date": target,
                "sales": sales_df.to_dict("records"),
                "popular_items": popular_df.to_dict("records"),
                "category_sales": cat_df.to_dict("records"),
            }
            json_path = self._file_svc.get_export_path(f"report_{target}.json")
            self._file_svc.export_json(json_path, json_data)
            paths["json"] = json_path

            logger.info("Full report exported for %s → %s", target, list(paths.keys()))
            return paths

        except Exception as exc:
            raise ReportGenerationError("full_report", str(exc)) from exc
