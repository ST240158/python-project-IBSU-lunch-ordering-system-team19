# IBSU Lunch Ordering System

# IBSU Lunch Ordering System

## Team Members

| Name | Student ID | Role |
|---|---|---|
| Gunther Darius | ST240158 | Lead Developer |
| Johannesh Pesh | T240723 | Database / QA |
| [Member 3] | [ID] | Documentation / Testing |

## Project

**Course:** IT0206 � Advanced Computer Programming 2  
**Assessment:** Assessment 2C � Capstone Project  
**Project:** IBSU Lunch Ordering System


A Python 3.x, menu-driven console application for campus lunch ordering. The implementation follows MVC separation, object-oriented design, a relational database, parameterized SQL, secure password hashing, CSV/JSON file handling, pytest testing, and administrator reporting with pandas/matplotlib/tabulate.

## Roles
- **Student/Customer:** view/search the menu, place orders, view own orders, and cancel an eligible `received` order.
- **Cafeteria Administrator:** add/view/edit/delete food items, view/search orders, update order status, and generate reports.

## Order statuses
The system defines exactly four persistent statuses: `received`, `preparing`, `ready`, and `collected`. Cancellation is not a fifth status; an eligible received order is removed transactionally and reserved stock is restored.

## Scope exclusions
No GUI, web/mobile application, online ordering platform, payment gateway, delivery tracking, supplier management, or separate inventory-management module is implemented. Stock is maintained only as a food-item availability field required for ordering.

## Setup
```text
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
pytest -q
```

SQLite is the default backend. `config.json` can select MySQL and provide connection settings. The MySQL schema is available at `database/mysql_schema.sql`.

## Demo accounts
- Student: `student` / `student123`
- Administrator: `admin` / `admin123`

These are assessment/demo credentials only. Passwords are stored as salted PBKDF2 hashes.
"# python-project-lunch-ordering-system" 
"# python-project-lunch-ordering-system" 
