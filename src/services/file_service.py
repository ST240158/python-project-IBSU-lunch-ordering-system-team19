"""FileService — CSV, JSON, and plain-text file handling.

Demonstrates Python's ``csv``, ``json``, and built-in file I/O.
All operations use the ``with`` statement for safe resource management.
"""

import csv
import json
import os
import logging
from datetime import datetime
from typing import Any

from ..exceptions.custom_exceptions import FileOperationError

logger = logging.getLogger("ibsu_lunch")


class FileService:
    """Handles all file import/export operations for the system.

    Supports CSV read/write, JSON read/write, and plain-text report export.
    """

    def __init__(self, base_dir: str = "data") -> None:
        self._base_dir = base_dir
        os.makedirs(os.path.join(base_dir, "imports"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "exports"), exist_ok=True)

    # ------------------------------------------------------------------ #
    # CSV                                                                  #
    # ------------------------------------------------------------------ #

    def import_csv(self, filepath: str) -> list[dict]:
        """Read a CSV file and return rows as a list of dictionaries.

        Args:
            filepath: Path to the CSV file.

        Returns:
            List of row dicts keyed by header names.

        Raises:
            FileOperationError: If the file cannot be read.
        """
        try:
            with open(filepath, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                rows = [row for row in reader]
            logger.info("CSV imported: %s (%d rows).", filepath, len(rows))
            return rows
        except FileNotFoundError as exc:
            raise FileOperationError(filepath, "read", "File not found.") from exc
        except csv.Error as exc:
            raise FileOperationError(filepath, "read", str(exc)) from exc

    def export_csv(self, filepath: str, data: list[dict], fieldnames: list[str] | None = None) -> None:
        """Write a list of dictionaries to a CSV file.

        Args:
            filepath: Destination path.
            data: Rows to write.
            fieldnames: Column order (auto-detected from first row if None).

        Raises:
            FileOperationError: If the file cannot be written.
        """
        try:
            if not data:
                logger.warning("No data to export to %s.", filepath)
                return
            if fieldnames is None:
                fieldnames = list(data[0].keys())
            with open(filepath, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logger.info("CSV exported: %s (%d rows).", filepath, len(data))
        except (OSError, csv.Error) as exc:
            raise FileOperationError(filepath, "write", str(exc)) from exc

    # ------------------------------------------------------------------ #
    # JSON                                                                 #
    # ------------------------------------------------------------------ #

    def import_json(self, filepath: str) -> Any:
        """Read a JSON file and return the parsed object.

        Args:
            filepath: Path to the JSON file.

        Returns:
            Parsed JSON (dict, list, etc.).

        Raises:
            FileOperationError: If the file cannot be read.
        """
        try:
            with open(filepath, encoding="utf-8") as fh:
                data = json.load(fh)
            logger.info("JSON imported: %s.", filepath)
            return data
        except FileNotFoundError as exc:
            raise FileOperationError(filepath, "read", "File not found.") from exc
        except json.JSONDecodeError as exc:
            raise FileOperationError(filepath, "read", f"Invalid JSON: {exc}") from exc

    def export_json(self, filepath: str, data: Any) -> None:
        """Write a Python object to a JSON file.

        Raises:
            FileOperationError: If the file cannot be written.
        """
        try:
            with open(filepath, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, default=str)
            logger.info("JSON exported: %s.", filepath)
        except (OSError, TypeError) as exc:
            raise FileOperationError(filepath, "write", str(exc)) from exc

    # ------------------------------------------------------------------ #
    # Plain-text reports                                                   #
    # ------------------------------------------------------------------ #

    def export_text_report(self, filepath: str, content: str) -> None:
        """Write a plain-text report file.

        Raises:
            FileOperationError: If the file cannot be written.
        """
        try:
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write(content)
            logger.info("Text report exported: %s.", filepath)
        except OSError as exc:
            raise FileOperationError(filepath, "write", str(exc)) from exc

    def append_text_report(self, filepath: str, content: str) -> None:
        """Append to a plain-text file (e.g., activity log)."""
        try:
            with open(filepath, "a", encoding="utf-8") as fh:
                fh.write(content + "\n")
        except OSError as exc:
            raise FileOperationError(filepath, "append", str(exc)) from exc

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def get_export_path(self, filename: str) -> str:
        """Return a full path inside the exports directory with a timestamp."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base, ext = os.path.splitext(filename)
        return os.path.join(self._base_dir, "exports", f"{base}_{ts}{ext}")

    def get_import_path(self, filename: str) -> str:
        """Return a full path inside the imports directory."""
        return os.path.join(self._base_dir, "imports", filename)
