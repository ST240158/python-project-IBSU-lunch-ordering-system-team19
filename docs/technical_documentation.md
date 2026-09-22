# Technical Documentation — IBSU Lunch Ordering System

## Architecture
The application is a menu-driven console program using MVC separation. Models represent domain entities and validation of persisted data; Views handle console presentation and input; Controllers orchestrate workflows and authorization. Repository classes provide Model-layer database access, while services handle authentication, file handling and reporting.

## Roles and scope
Exactly two roles are implemented: Student/Customer and Cafeteria Administrator. Persistent order statuses are exactly `received`, `preparing`, `ready`, and `collected`. Cancellation of a `received` order is implemented as a transaction that removes the order and restores reserved stock because the prompt does not define a cancelled status.

The system intentionally excludes GUI/web/mobile interfaces, payment processing, delivery tracking, supplier management and a separate inventory-management module. Food-item stock is retained because availability/stock is part of the ordering domain.

## Security
All application SQL uses parameterized values. Passwords are stored using salted PBKDF2-HMAC-SHA256 with a per-password random salt and 310,000 iterations. Raw database exceptions are not intended for end users.

## Database
SQLite is the default development backend. `DatabaseManager` also supports MySQL through `mysql-connector-python`. The standalone schemas are `database/schema.sql` and `database/mysql_schema.sql`.

## File handling
`FileService` handles CSV, JSON and text output using context managers. CSV/JSON menu import and order/report export are supported. `config.json` selects the database backend and report output settings.

## Reporting
Administrator reports use pandas for analysis, matplotlib for saved charts, and tabulate for console presentation. Reports include daily collected-order sales, popular food items, category sales, and order-status counts.

## Testing
Run `pytest -q`. The current clean test run in this review produced **158 passed, 0 failed**. The date-search test was corrected to use the current date instead of a stale hard-coded date.

## Known implementation decisions
1. The prompt names StudentCustomer and Administrator role-specific IDs; the existing schema uses `users.user_id` as the identity key and the domain StudentCustomer/Admin IDs are derived from that key.
2. The prompt allows MySQL or SQLite and the project defaults to SQLite for simple deployment; MySQL support is provided as an alternative backend.
3. Cancellation is represented by transactional deletion because the prompt fixes the persistent status set to four values and does not define `cancelled`.
