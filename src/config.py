"""Application configuration constants.

Centralises paths, default values, and tuning knobs so they are not
scattered throughout the codebase.
"""

import os

# --------------------------------------------------------------------------- #
# Paths                                                                        #
# --------------------------------------------------------------------------- #
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "ibsu_lunch.db")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
IMPORT_DIR = os.path.join(DATA_DIR, "imports")
EXPORT_DIR = os.path.join(DATA_DIR, "exports")

# --------------------------------------------------------------------------- #
# Database                                                                      #
# --------------------------------------------------------------------------- #
DB_SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

# --------------------------------------------------------------------------- #
# Defaults                                                                      #
# --------------------------------------------------------------------------- #
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_STUDENT_USERNAME = "student"
DEFAULT_STUDENT_PASSWORD = "student123"

# --------------------------------------------------------------------------- #
# Validation                                                                    #
# --------------------------------------------------------------------------- #
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 30
MIN_PASSWORD_LENGTH = 6
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 100

# --------------------------------------------------------------------------- #
# Logging                                                                       #
# --------------------------------------------------------------------------- #
LOG_FILE = os.path.join(LOG_DIR, "ibsu_lunch.log")
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# JSON configuration
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DB_BACKEND = "sqlite"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "ibsu_lunch"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
