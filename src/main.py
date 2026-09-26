"""IBSU Lunch Ordering System — Entry Point.

Run with::

    python -m src.main

or::

    cd Assessment2 && python src/main.py
"""

import os
import sys
import json
from src.config import CONFIG_PATH
from src.repositories.database import DatabaseManager

# Ensure the project root is on sys.path so ``src`` is importable
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.utils.logger import setup_logger
from src.controllers.main_controller import MainController


def main() -> None:
    """Bootstrap logging and launch the application."""
    setup_logger()
    config = {}
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as fh:
            config = json.load(fh)
    app = MainController(DatabaseManager.from_config(config) if config else None)
    app.run()


if __name__ == "__main__":
    main()
