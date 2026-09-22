# IT0206 Assessment 2 — Database Design
## IBSU Lunch Ordering System

### 1. Database Technology

SQLite is used as the relational database. The application creates the database automatically, while `database/schema.sql` provides a reproducible standalone schema and seed-data script.

### 2. Tables

| Table | Primary key | Important foreign keys | Purpose |
|---|---|---|---|
| `users` | `user_id` | — | Authentication, identity and role |
| `category` | `category_id` | — | Menu classification |
| `food_items` | `food_item_id` | `category_id → category` | Menu items, price and stock |
| `orders` | `order_id` | `user_id → users`, `status_id → order_status` | Customer order header |
| `order_items` | `order_item_id` | `order_id → orders`, `food_item_id → food_items` | Order line items |
| `order_status` | `status_id` | — | Controlled order status values |

### 3. Relationships

- One user can have many orders.
- One order can have many order items.
- One food item can appear in many order items.
- One category can contain many food items.
- One order status can apply to many orders.

### 4. Normalisation

The schema separates independent entities and uses foreign keys rather than repeating category, user or status data in order/menu records. `order_items.item_name`, `unit_price` and `subtotal` are intentionally stored as order-time snapshots so historical order information remains stable if a menu item is later renamed or repriced.

### 5. Integrity Constraints

- `username` is unique.
- User role is restricted to `student` or `admin`.
- Food price and stock cannot be negative.
- Order-item quantity must be greater than zero.
- Foreign keys are enabled.
- Status names are unique.

### 6. CRUD and Transactions

Repositories perform parameterised `INSERT`, `SELECT`, `UPDATE` and `DELETE` operations. Order creation and cancellation/deletion use explicit transactions so related changes are committed together or rolled back on failure.

### 7. Reproduction

From the project root:

```bash
sqlite3 database/ibsu_lunch.db < database/schema.sql
```

If the SQLite CLI is unavailable, the same script can be executed with Python's built-in `sqlite3` module.

### 8. Diagram

See `docs/diagrams/erd.png` for the implemented ER diagram.
