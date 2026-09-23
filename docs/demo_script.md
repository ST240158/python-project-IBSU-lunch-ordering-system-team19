# IT0206 Assessment 2C — Presentation and Demonstration Script
## IBSU Lunch Ordering System

**Target duration:** 10–15 minutes  
**Presenter:** Gunther Darius / assigned team member

### 0:00–0:45 — Introduction

> Good morning/afternoon. Our project is the IBSU Lunch Ordering System, a menu-driven Python application designed for a campus cafeteria. The system provides students with a simple ordering workflow and gives administrators tools for menu, stock, order and reporting management.

### 0:45–1:30 — Problem, Aim and Objectives

> The problem we addressed is the difficulty of managing menu information, stock and orders through manual processes. Our aim was to design and deliver a persistent, role-based Python application using professional software engineering practices.

Mention the objectives briefly: authentication, roles, CRUD, transactional ordering, search, reporting, file handling, logging and testing.

### 1:30–2:30 — Architecture and OOP

Show the MVC diagram.

> The application follows MVC and a layered architecture. Views handle console interaction, controllers orchestrate requests, services implement cross-cutting operations, repositories handle SQLite access, and models represent the domain.

Explain:
- `User` is an abstract base class.
- `Student` and `Administrator` inherit from it.
- Role-specific methods demonstrate polymorphism and overriding.
- `Order` contains `OrderItem` objects, demonstrating composition.
- Properties provide controlled attribute access.

### 2:30–3:15 — Database

Show ERD.

> The database contains six related tables: users, category, food_items, orders, order_items and order_status. Foreign keys maintain relationships, while parameterised queries protect against SQL injection. Order creation and cancellation use transactions.

### 3:15–5:00 — Student Demonstration

Run:

```bash
python -m src.main
```

Use:

```text
Student: student
Password: student123
```

Demonstrate:
1. Login.
2. Browse menu.
3. Place an order for one or two items.
4. Show order ID and total.
5. View order history.
6. Cancel the order.
7. Explain that eligible cancellation restores stock.

Suggested narration:

> The student cannot access administrator functions because the authenticated role determines the available menu and permissions.

### 5:00–7:30 — Administrator Demonstration

Login:

```text
Administrator: admin
Password: admin123
```

Demonstrate:
1. View all orders.
2. Update an order status to collected.
3. Manage menu items — show add/update/delete/search.
4. Open reports.
5. Generate daily sales, popular-items and category reports.
6. Generate charts.
7. Export full report.

Suggested narration:

> The repository layer keeps raw SQL out of the console views. Reporting is performed by the service layer using pandas, while matplotlib provides the visualisations.

### 7:30–8:30 — File Handling and External API

Show:
- `sample_menu.csv`
- `sample_menu.json`
- generated TXT/CSV/JSON reports
- chart PNG files

> CSV and JSON support interoperability and backup/migration scenarios. The application uses CSV/JSON file handling and local reporting; no external HTTP service is required.

### 8:30–9:30 — Testing

Run/show:

```bash
python -m pytest -q
```

Say:

> The final automated suite contains 159 passing tests with zero failures. Core models, repositories, services, validation and database schema reproduction are covered. Core-source coverage is 81 percent. Interactive controllers and views are additionally verified through functional end-to-end testing.

### 9:30–10:30 — Professional Practice

Discuss:
- logging
- custom exceptions
- parameterised SQL
- documentation
- Git/GitHub
- privacy
- copyright
- AI disclosure

Important wording:

> AI assistance was used transparently for code review, debugging suggestions, documentation and presentation preparation. We verified and tested the submitted implementation and can explain the design decisions.

### 10:30–11:30 — Limitations/Future Work

Mention:
- Argon2/bcrypt for production passwords.
- GUI/web interface.
- online payment integration.
- cloud database/deployment.
- richer analytics.

### 11:30–12:00 — Conclusion

> The project demonstrates a complete professional Python application from requirements and design through implementation, database integration, testing, documentation and delivery. The core workflows are working and the final package is prepared for GitHub publication and assessment submission.

### Likely Q&A

**Why MVC?**  
To separate presentation, control and domain/data responsibilities, improving maintainability and testing.

**Why repository pattern?**  
To isolate SQL and database access from controllers and views.

**How is stock protected?**  
Order creation checks stock and performs stock updates and order inserts in one transaction.

**Why use PBKDF2 password hashing?**  
It is retained for this academic implementation; production password storage should use Argon2/bcrypt with salts.

**What happens if the API is offline?**  
The application does not depend on an external HTTP service, so core functionality remains available offline.

**How did you test the application?**  
Automated pytest tests cover core logic/data access and negative paths, while manual functional testing covers the interactive end-to-end workflows. UAT requires a real tester sign-off.
