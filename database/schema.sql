-- IBSU Lunch Ordering System — reproducible SQLite schema and seed data
-- Usage from the project root:
--   sqlite3 database/ibsu_lunch.db < database/schema.sql
-- The application itself can also create the same schema automatically.

PRAGMA foreign_keys = ON;

-- Drop child tables before parent tables so the script can be safely rebuilt.
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS food_items;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS order_status;

CREATE TABLE order_status (
    status_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    status_name TEXT NOT NULL UNIQUE
);

CREATE TABLE category (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    description   TEXT DEFAULT ''
);

CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('student', 'admin')),
    name          TEXT NOT NULL DEFAULT '',
    contact_info  TEXT DEFAULT '',
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE food_items (
    food_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id  INTEGER NOT NULL,
    name         TEXT NOT NULL,
    description  TEXT DEFAULT '',
    price        REAL NOT NULL CHECK (price >= 0),
    stock        INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    order_date   TEXT NOT NULL DEFAULT (datetime('now')),
    status_id    INTEGER NOT NULL DEFAULT 1,
    total_amount REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (status_id) REFERENCES order_status(status_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      INTEGER NOT NULL,
    food_item_id  INTEGER NOT NULL,
    item_name     TEXT NOT NULL,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    REAL NOT NULL CHECK (unit_price >= 0),
    subtotal      REAL NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (food_item_id) REFERENCES food_items(food_item_id)
);

-- Lookup/status seed data.
INSERT INTO order_status (status_name) VALUES
    ('received'), ('preparing'), ('ready'), ('collected');

-- Demo credentials (admin123 / student12)
INSERT INTO users (username, password_hash, role, name, contact_info) VALUES
    ('admin', 'pbkdf2_sha256$310000$00112233445566778899aabbccddeeff$d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592', 'admin', 'System Administrator', ''),
    ('student', 'pbkdf2_sha256$310000$ffeeddccbbaa99887766554433221100$ad8e44d4a8d7f3783de6b99ebd5d90e154dd5b7f19cf2c91c67d6ecfa37d69b3', 'student', 'Demo Student', 'student@ibsu.edu');
    
INSERT INTO category (category_name, description) VALUES
    ('Main Dish', 'Hearty main courses'),
    ('Side Dish', 'Accompaniments and sides'),
    ('Beverage', 'Drinks and refreshments'),
    ('Dessert', 'Sweet treats'),
    ('Salad', 'Fresh salads');

INSERT INTO food_items (category_id, name, description, price, stock) VALUES
    (1, 'Grilled Chicken', 'Juicy grilled chicken breast', 7.50, 50),
    (1, 'Beef Stew', 'Hearty beef stew with vegetables', 8.00, 40),
    (1, 'Vegetable Pasta', 'Penne with seasonal veggies', 6.50, 35),
    (2, 'French Fries', 'Crispy golden fries', 3.00, 80),
    (2, 'Mashed Potatoes', 'Creamy mashed potatoes', 3.50, 60),
    (3, 'Orange Juice', 'Fresh-squeezed orange juice', 2.50, 100),
    (3, 'Coffee', 'Hot brewed coffee', 2.00, 120),
    (3, 'Mineral Water', 'Still mineral water', 1.50, 200),
    (4, 'Chocolate Cake', 'Rich chocolate layer cake', 4.50, 30),
    (4, 'Fruit Salad', 'Mixed seasonal fruits', 3.50, 45),
    (5, 'Caesar Salad', 'Classic Caesar with croutons', 5.50, 40),
    (5, 'Greek Salad', 'Tomatoes, cucumber, olives, feta', 5.00, 35);