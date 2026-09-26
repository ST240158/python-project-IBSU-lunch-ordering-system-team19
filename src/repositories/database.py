"""DatabaseManager for SQLite (default) and MySQL development targets."""

import logging
import os
import sqlite3
from typing import Any, Optional

from ..exceptions.custom_exceptions import DatabaseConnectionError

logger = logging.getLogger("ibsu_lunch")


class DatabaseManager:
    """Centralise database connections, schema bootstrap and transactions.

    SQLite is the default development backend. MySQL is supported when the
    optional ``mysql-connector-python`` dependency is installed and the
    corresponding connection settings are supplied.
    """

    _instance: Optional["DatabaseManager"] = None

    def __init__(self, db_path: str = "", backend: str = "sqlite", **mysql_config: Any) -> None:
        self._backend = backend.lower()
        self._mysql_config = mysql_config
        if self._backend == "sqlite":
            if not db_path:
                db_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    "database", "ibsu_lunch.db",
                )
            self._db_path = db_path
        elif self._backend == "mysql":
            self._db_path = "mysql"
        else:
            raise ValueError("Database backend must be 'sqlite' or 'mysql'.")
        self._conn = None

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "DatabaseManager":
        """Build a manager from the application's JSON configuration."""
        db = config.get("database", {})
        backend = str(db.get("backend", "sqlite")).lower()
        if backend == "mysql":
            return cls(backend="mysql", **db.get("mysql", {}))
        return cls(db_path=str(db.get("sqlite_path", "database/ibsu_lunch.db")), backend="sqlite")

    @classmethod
    def get_instance(cls, db_path: str = "", backend: str = "sqlite", **mysql_config: Any) -> "DatabaseManager":
        """Return the shared DatabaseManager instance."""
        if cls._instance is None:
            cls._instance = cls(db_path, backend, **mysql_config)
        return cls._instance

    @property
    def backend(self) -> str:
        """Return the active database backend."""
        return self._backend

    @property
    def db_path(self) -> str:
        """Return the SQLite path or ``mysql`` for the MySQL backend."""
        return self._db_path

    def connect(self):
        """Open a connection to the selected database backend."""
        try:
            if self._backend == "sqlite":
                os.makedirs(os.path.dirname(self._db_path) or ".", exist_ok=True)
                self._conn = sqlite3.connect(self._db_path)
                self._conn.row_factory = sqlite3.Row
                self._conn.execute("PRAGMA foreign_keys = ON")
            else:
                import mysql.connector
                self._conn = mysql.connector.connect(
                    host=self._mysql_config.get("host", "localhost"),
                    port=int(self._mysql_config.get("port", 3306)),
                    database=self._mysql_config.get("database", "ibsu_lunch"),
                    user=self._mysql_config.get("user", "root"),
                    password=self._mysql_config.get("password", ""),
                )
            logger.info("Database connected using %s.", self._backend)
            return self._conn
        except Exception as exc:
            raise DatabaseConnectionError(self._db_path) from exc

    @property
    def connection(self):
        """Return the active connection, connecting lazily if necessary."""
        if self._conn is None:
            self.connect()
        return self._conn

    def close(self) -> None:
        """Close the current connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def initialize_schema(self) -> None:
        """Create the application schema and seed the four valid statuses."""
        conn = self.connection
        try:
            if self._backend == "sqlite":
                conn.executescript(self._sqlite_schema())
                conn.commit()
            else:
                cursor = conn.cursor()
                for statement in self._mysql_schema().split(";"):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        logger.info("Database schema initialised / verified.")

    @staticmethod
    def _sqlite_schema() -> str:
        return """
        CREATE TABLE IF NOT EXISTS order_status (
            status_id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            description TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'admin')),
            name TEXT NOT NULL DEFAULT '',
            contact_info TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS food_items (
            food_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            price REAL NOT NULL CHECK(price >= 0),
            stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
            FOREIGN KEY (category_id) REFERENCES category(category_id)
        );
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status_id INTEGER NOT NULL DEFAULT 1,
            total_amount REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (status_id) REFERENCES order_status(status_id)
        );
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            food_item_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL CHECK(unit_price >= 0),
            subtotal REAL NOT NULL CHECK(subtotal >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (food_item_id) REFERENCES food_items(food_item_id)
        );
        INSERT OR IGNORE INTO order_status(status_id, status_name) VALUES
            (1, 'received'), (2, 'preparing'), (3, 'ready'), (4, 'collected');
        """

    @staticmethod
    def _mysql_schema() -> str:
        return """
        CREATE TABLE IF NOT EXISTS order_status (status_id INT AUTO_INCREMENT PRIMARY KEY, status_name VARCHAR(30) NOT NULL UNIQUE);
        CREATE TABLE IF NOT EXISTS category (category_id INT AUTO_INCREMENT PRIMARY KEY, category_name VARCHAR(100) NOT NULL UNIQUE, description TEXT);
        CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, role VARCHAR(20) NOT NULL, name VARCHAR(100) NOT NULL, contact_info VARCHAR(255), CHECK (role IN ('student','admin')));
        CREATE TABLE IF NOT EXISTS food_items (food_item_id INT AUTO_INCREMENT PRIMARY KEY, category_id INT NOT NULL, name VARCHAR(150) NOT NULL, description TEXT, price DECIMAL(10,2) NOT NULL CHECK (price >= 0), stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0), FOREIGN KEY (category_id) REFERENCES category(category_id));
        CREATE TABLE IF NOT EXISTS orders (order_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, order_date DATETIME NOT NULL, status_id INT NOT NULL DEFAULT 1, total_amount DECIMAL(10,2) NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (status_id) REFERENCES order_status(status_id));
        CREATE TABLE IF NOT EXISTS order_items (order_item_id INT AUTO_INCREMENT PRIMARY KEY, order_id INT NOT NULL, food_item_id INT NOT NULL, item_name VARCHAR(150) NOT NULL, quantity INT NOT NULL CHECK (quantity > 0), unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0), subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0), FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE, FOREIGN KEY (food_item_id) REFERENCES food_items(food_item_id));
        INSERT IGNORE INTO order_status(status_id, status_name) VALUES (1,'received'),(2,'preparing'),(3,'ready'),(4,'collected');
        """

    def _adapt_sql(self, sql: str) -> str:
        return sql.replace("?", "%s") if self._backend == "mysql" else sql

    def begin_transaction(self) -> None:
        self.connection.start_transaction() if self._backend == "mysql" else self.connection.execute("BEGIN")

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    def execute_query(self, sql: str, params: tuple = ()) -> list[dict]:
        """Execute a SELECT using parameterized values and return dictionaries."""
        cursor = self.connection.cursor(dictionary=True) if self._backend == "mysql" else self.connection.cursor()
        cursor.execute(self._adapt_sql(sql), params)
        rows = cursor.fetchall()
        if self._backend == "mysql":
            cursor.close()
            return [dict(row) for row in rows]
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def execute_update(self, sql: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected-row count."""
        cursor = self.connection.cursor()
        cursor.execute(self._adapt_sql(sql), params)
        count = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return count

    def execute_insert(self, sql: str, params: tuple = ()) -> int:
        """Execute an INSERT and return its generated primary key."""
        cursor = self.connection.cursor()
        cursor.execute(self._adapt_sql(sql), params)
        last_id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return int(last_id)

    def __enter__(self) -> "DatabaseManager":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        self.close()

    def __repr__(self) -> str:
        return f"DatabaseManager(backend='{self._backend}')"
