# IT0206 Assessment 2C — Project Proposal
## IBSU Lunch Ordering System

**Course:** IT0206 — Advanced Computer Programming 2  
**Assessment:** Team Project — Designing, Building, and Delivering a Professional Python Application  
**Primary student:** Gunther Darius — ST240158  
**Other team members:** [Team Member 2 — ID], [Team Member 3 — ID]  
**Project domain:** Restaurant Ordering System / Campus Lunch Ordering  

### 1. Problem Statement

Campus cafeteria ordering can become inefficient when menu information, stock availability and order tracking are handled manually. Students need a simple way to view available food and place orders, while cafeteria administrators need reliable tools for menu management, stock control, order status tracking and reporting.

### 2. Proposed Solution

The IBSU Lunch Ordering System is a menu-driven Python console application that provides authenticated, role-based access for students and administrators. Students can browse the menu, place orders, view order history and cancel eligible orders. Administrators can manage categories and menu items, monitor orders, update order status, import menu data, export records and generate reports and charts.

### 3. Aim

To design, build, test and deliver a professional Python application that digitises the campus lunch-ordering workflow while demonstrating object-oriented programming, MVC architecture, relational database programming, file handling, exception handling, testing and professional software engineering practices.

### 4. Objectives

1. Implement secure username/password authentication using hashed credentials.
2. Provide at least two roles with differentiated permissions: Student and Administrator.
3. Implement a navigable console interface with input validation and graceful error handling.
4. Provide CRUD operations for core domain entities including categories, menu items and orders.
5. Implement transactional order placement and stock restoration for eligible cancellations/deletions.
6. Provide search/filter functions and management reports using pandas and matplotlib.
7. Support CSV, JSON and plain-text file handling.
8. Implement application-wide logging and custom exceptions.
9. Develop automated pytest tests and document functional and UAT testing.
10. Deliver professional documentation, a reproducible SQL script, GitHub repository and recorded/live demonstration.

### 5. Scope

**In scope:** authentication, student ordering, order cancellation, menu/category CRUD, order management, stock management, reporting, CSV/JSON import/export, SQLite persistence, logging, automated testing and documentation.

**Out of scope:** online payment processing, real-time delivery tracking, production cloud deployment, mobile application and integration with an institutional student information system.

### 6. Feasibility

- **Technical:** Python 3.11+, SQLite/MySQL, pytest, pandas, matplotlib and tabulate are sufficient for the required features.
- **Operational:** The console workflow is simple enough for students and cafeteria administrators to use after a short orientation.
- **Economic:** The selected technologies are free/open-source and SQLite requires no database server.
- **Schedule:** The solution aligns with the seven-week SDLC structure in the assessment brief.

### 7. Stakeholders and Roles

| Stakeholder | Interest |
|---|---|
| Students | Browse menu, place and track lunch orders |
| Cafeteria administrators | Manage menu, stock and orders; produce reports |
| Lecturer/marker | Assess functionality, architecture, testing and delivery |
| Project team | Analyse, develop, test, document and present the system |

### 8. Team Roles

| Member | Primary role | Responsibility |
|---|---|---|
| Gunther Darius — ST240158 | Lead Developer / Architect | MVC, OOP, integration and final consolidation |
| [Member 2] | Database / Backend | Schema, repositories, database testing |
| [Member 3] | QA / Documentation | Test plan, UAT, user manual and technical documentation |

> Replace placeholders with the registered team details before submission.
