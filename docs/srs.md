# Software Requirements Specification — IBSU Lunch Ordering System

## Functional requirements
- **FR-01:** Display a console main menu with Student Login, Administrator Login and Exit.
- **FR-02:** Authenticate Student/Customer and Cafeteria Administrator accounts using secure password hashes.
- **FR-03:** Enforce role-based authorization in Controllers.
- **FR-04:** Students can view and search food items by name/category.
- **FR-05:** Students can create orders containing one or more food items and quantities.
- **FR-06:** The system calculates item subtotals and order totals automatically.
- **FR-07:** The system stores orders and order items transactionally and reserves stock.
- **FR-08:** Students can view their own previous/current orders.
- **FR-09:** Students can cancel an order only while its status is `received`; cancellation restores stock transactionally.
- **FR-10:** Administrators can add, view, edit and delete food items and manage categories through administrative subflows.
- **FR-11:** Administrators can view/search orders by student, date and status.
- **FR-12:** Administrators can update an order to one of exactly four statuses: `received`, `preparing`, `ready`, `collected`.
- **FR-13:** The system supports CSV export, JSON configuration and optional CSV/JSON menu import.
- **FR-14:** The system generates reports using pandas, matplotlib and tabulate.
- **FR-15:** The system records application events through logging and handles expected errors with custom exceptions.

## Non-functional requirements
- Python 3.x.
- MVC separation: View does not access the database directly; database logic remains in the Model/repository layer.
- Parameterized SQL for user/application data.
- Passwords are never stored as plaintext.
- SQLite is the default development backend; MySQL is supported as an alternative.
- File operations use context managers.
- Automated tests use pytest.

## Out of scope
GUI, web application, mobile application, online ordering platform, payment gateway, delivery tracking, supplier management and separate inventory-management functionality.

## Implementation decisions
The prompt does not define a `cancelled` status. Cancellation is therefore implemented by removing an eligible `received` order and restoring reserved stock. The prompt also allows SQLite or MySQL, so SQLite is the default and MySQL is an alternative backend.
