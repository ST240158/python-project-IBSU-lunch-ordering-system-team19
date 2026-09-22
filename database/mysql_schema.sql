-- IBSU Lunch Ordering System — MySQL schema
CREATE DATABASE IF NOT EXISTS ibsu_lunch;
USE ibsu_lunch;

CREATE TABLE IF NOT EXISTS order_status (status_id INT AUTO_INCREMENT PRIMARY KEY, status_name VARCHAR(30) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS category (category_id INT AUTO_INCREMENT PRIMARY KEY, category_name VARCHAR(100) NOT NULL UNIQUE, description TEXT);
CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, role VARCHAR(20) NOT NULL, name VARCHAR(100) NOT NULL, contact_info VARCHAR(255), CHECK (role IN ('student','admin')));
CREATE TABLE IF NOT EXISTS food_items (food_item_id INT AUTO_INCREMENT PRIMARY KEY, category_id INT NOT NULL, name VARCHAR(150) NOT NULL, description TEXT, price DECIMAL(10,2) NOT NULL CHECK (price >= 0), stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0), FOREIGN KEY (category_id) REFERENCES category(category_id));
CREATE TABLE IF NOT EXISTS orders (order_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, order_date DATETIME NOT NULL, status_id INT NOT NULL DEFAULT 1, total_amount DECIMAL(10,2) NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (status_id) REFERENCES order_status(status_id));
CREATE TABLE IF NOT EXISTS order_items (order_item_id INT AUTO_INCREMENT PRIMARY KEY, order_id INT NOT NULL, food_item_id INT NOT NULL, item_name VARCHAR(150) NOT NULL, quantity INT NOT NULL CHECK (quantity > 0), unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0), subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0), FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE, FOREIGN KEY (food_item_id) REFERENCES food_items(food_item_id));
INSERT IGNORE INTO order_status(status_id, status_name) VALUES (1,'received'),(2,'preparing'),(3,'ready'),(4,'collected');
