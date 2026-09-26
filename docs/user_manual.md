# IBSU Lunch Ordering System — User Manual

## Main menu
1. Student Login
2. Administrator Login
3. Exit

## Student/Customer
After Student Login:
1. View Menu
2. Search Food
3. Place Order
4. View My Orders
5. Cancel Order
6. Logout

Only an order with status `received` can be cancelled. Cancellation removes the order and restores the reserved stock because the system defines only four persistent statuses.

## Cafeteria Administrator
After Administrator Login:
1. Add Food Item
2. View Food Items
3. Edit Food Item
4. Delete Food Item
5. View Orders
6. Update Order Status
7. Generate Reports
8. Logout

Order search is available from View Orders. Category management and CSV/JSON menu import are available through administrative subflows. Reporting includes daily collected-order sales, popular items and category sales, with matplotlib charts and export options.

## Demo accounts
- Student: `student` / `student123`
- Administrator: `admin` / `admin123`

These credentials are for assessment demonstration only.
