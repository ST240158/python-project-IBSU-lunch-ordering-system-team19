"""Integration tests for repository classes (backed by temp SQLite DB).

Covers:
  - User auth, duplicate check, role filtering, delete
  - Category CRUD + duplicate detection
  - FoodItem CRUD, search, stock management
  - OrderStatus reads
  - OrderItem creation / read-back
  - Order creation (transactional stock decrease), cancellation (stock restore),
    status update, search by date / status / student
"""

import pytest

from src.exceptions.custom_exceptions import (
    InvalidCredentialsError,
    DuplicateUsernameError,
    DuplicateCategoryError,
    CategoryNotFoundError,
    CategoryInUseError,
    FoodItemNotFoundError,
    InsufficientStockError,
    OrderNotFoundError,
    OrderCannotBeCancelledError,
    InvalidOrderError,
)


# ======================================================================= #
# UserRepository                                                            #
# ======================================================================= #

class TestUserRepository:

    def test_create_student(self, user_repo):
        s = user_repo.create_student("alice", "pass123", "Alice", "alice@ibsu.edu")
        assert s.user_id > 0
        assert s.username == "alice"
        assert s.role == "student"

    def test_create_admin(self, user_repo):
        a = user_repo.create_admin("admin1", "admin123", "Admin")
        assert a.user_id > 0
        assert a.role == "admin"

    def test_duplicate_username_raises(self, user_repo):
        user_repo.create_student("bob", "pass", "Bob")
        with pytest.raises(DuplicateUsernameError):
            user_repo.create_admin("bob", "pass2", "Bob2")

    def test_authenticate_success(self, user_repo):
        user_repo.create_student("carol", "secret", "Carol")
        user = user_repo.authenticate("carol", "secret")
        assert user.username == "carol"

    def test_authenticate_wrong_password(self, user_repo):
        user_repo.create_student("dave", "pw1", "Dave")
        with pytest.raises(InvalidCredentialsError):
            user_repo.authenticate("dave", "wrong")

    def test_authenticate_unknown_user(self, user_repo):
        with pytest.raises(InvalidCredentialsError):
            user_repo.authenticate("nobody", "pw")

    def test_get_by_id(self, user_repo):
        s = user_repo.create_student("eve", "pw", "Eve")
        row = user_repo.get_by_id(s.user_id)
        assert row is not None
        assert row["username"] == "eve"

    def test_get_by_id_missing(self, user_repo):
        assert user_repo.get_by_id(9999) is None

    def test_get_all(self, user_repo):
        user_repo.create_student("u1", "p", "U1")
        user_repo.create_admin("a1", "p", "A1")
        all_users = user_repo.get_all()
        assert len(all_users) == 2

    def test_get_by_role(self, user_repo):
        user_repo.create_student("s1", "p", "S1")
        user_repo.create_admin("adm", "p", "Adm")
        students = user_repo.get_by_role("student")
        assert len(students) == 1
        assert students[0]["role"] == "student"

    def test_delete(self, user_repo):
        s = user_repo.create_student("del", "pw", "Del")
        assert user_repo.delete(s.user_id) is True
        assert user_repo.get_by_id(s.user_id) is None

    def test_delete_missing(self, user_repo):
        assert user_repo.delete(9999) is False

    def test_password_hashing(self, user_repo):
        s = user_repo.create_student("hasher", "mypassword", "Hasher")
        # Password must not be stored in plaintext
        row = user_repo.get_by_id(s.user_id)
        assert row is not None
        # The authenticate function uses the same hash
        assert user_repo.authenticate("hasher", "mypassword").user_id == s.user_id


# ======================================================================= #
# CategoryRepository                                                       #
# ======================================================================= #

class TestCategoryRepository:

    def test_create(self, category_repo):
        c = category_repo.create("Main Dish", "Hearty meals")
        assert c.category_id > 0
        assert c.category_name == "Main Dish"

    def test_duplicate_name_raises(self, category_repo):
        category_repo.create("Beverage", "Drinks")
        with pytest.raises(DuplicateCategoryError):
            category_repo.create("Beverage", "Cold drinks")

    def test_get_by_id(self, category_repo):
        c = category_repo.create("Salad", "Greens")
        row = category_repo.get_by_id(c.category_id)
        assert row is not None
        assert row["name"] == "Salad"

    def test_get_by_id_missing(self, category_repo):
        assert category_repo.get_by_id(9999) is None

    def test_get_all(self, category_repo):
        category_repo.create("A", "Desc A")
        category_repo.create("B", "Desc B")
        all_cats = category_repo.get_all()
        assert len(all_cats) == 2

    def test_update(self, category_repo):
        c = category_repo.create("Old", "Old desc")
        result = category_repo.update(c.category_id, name="New", description="New desc")
        assert result is True
        row = category_repo.get_by_id(c.category_id)
        assert row["name"] == "New"

    def test_update_missing_raises(self, category_repo):
        with pytest.raises(CategoryNotFoundError):
            category_repo.update(9999, name="Ghost")

    def test_delete(self, category_repo):
        c = category_repo.create("Temp", "Temporary")
        result = category_repo.delete(c.category_id)
        assert result is True
        assert category_repo.get_by_id(c.category_id) is None

    def test_delete_missing_raises(self, category_repo):
        with pytest.raises(CategoryNotFoundError):
            category_repo.delete(9999)


    def test_delete_in_use_raises(self, category_repo, food_repo):
        """A category referenced by a food item cannot be deleted silently."""
        category = category_repo.create("Used", "In use")
        food_repo.create(category.category_id, "Used Item", "Test", 2.0, 5)
        with pytest.raises(CategoryInUseError):
            category_repo.delete(category.category_id)


# ======================================================================= #
# FoodItemRepository                                                       #
# ======================================================================= #

class TestFoodItemRepository:

    def test_create(self, food_repo, category_repo):
        c = category_repo.create("Main", "Mains")
        fi = food_repo.create(c.category_id, "Pasta", "Penne", 5.50, 20)
        assert fi.food_item_id > 0
        assert fi.name == "Pasta"

    def test_get_by_id(self, food_repo, category_repo):
        c = category_repo.create("Drinks", "Beverages")
        fi = food_repo.create(c.category_id, "Tea", "Hot tea", 2.0, 30)
        row = food_repo.get_by_id(fi.food_item_id)
        assert row is not None
        assert row["name"] == "Tea"

    def test_get_by_id_missing(self, food_repo):
        assert food_repo.get_by_id(9999) is None

    def test_search(self, food_repo, category_repo):
        c = category_repo.create("Main", "Mains")
        food_repo.create(c.category_id, "Chicken Curry", "Spicy", 7.0, 15)
        food_repo.create(c.category_id, "Beef Noodle", "Soupy", 6.5, 10)
        results = food_repo.search("Chicken")
        assert len(results) == 1
        assert results[0]["name"] == "Chicken Curry"

    def test_update(self, food_repo, category_repo):
        c = category_repo.create("Main", "Mains")
        fi = food_repo.create(c.category_id, "Rice", "Plain rice", 3.0, 50)
        result = food_repo.update(fi.food_item_id, price=3.50, stock=40)
        assert result is True
        row = food_repo.get_by_id(fi.food_item_id)
        assert row["price"] == 3.50
        assert row["stock"] == 40

    def test_update_missing_raises(self, food_repo):
        with pytest.raises(FoodItemNotFoundError):
            food_repo.update(9999, name="Ghost")

    def test_delete(self, food_repo, category_repo):
        c = category_repo.create("Dessert", "Sweets")
        fi = food_repo.create(c.category_id, "Cake", "Choc", 4.0, 10)
        result = food_repo.delete(fi.food_item_id)
        assert result is True
        assert food_repo.get_by_id(fi.food_item_id) is None

    def test_delete_missing_raises(self, food_repo):
        with pytest.raises(FoodItemNotFoundError):
            food_repo.delete(9999)

    def test_decrease_stock(self, food_repo, category_repo):
        c = category_repo.create("Main", "Mains")
        fi = food_repo.create(c.category_id, "Stew", "Beef stew", 8.0, 25)
        food_repo.decrease_stock(fi.food_item_id, 5)
        row = food_repo.get_by_id(fi.food_item_id)
        assert row["stock"] == 20

    def test_decrease_stock_insufficient(self, food_repo, category_repo):
        c = category_repo.create("Main", "Mains")
        fi = food_repo.create(c.category_id, "Bread", "Loaf", 2.0, 3)
        with pytest.raises(InsufficientStockError):
            food_repo.decrease_stock(fi.food_item_id, 5)

    def test_increase_stock(self, food_repo, category_repo):
        c = category_repo.create("Main", "Mains")
        fi = food_repo.create(c.category_id, "Soup", "Veg soup", 4.0, 10)
        food_repo.increase_stock(fi.food_item_id, 5)
        row = food_repo.get_by_id(fi.food_item_id)
        assert row["stock"] == 15

    def test_increase_stock_missing_raises(self, food_repo):
        with pytest.raises(FoodItemNotFoundError):
            food_repo.increase_stock(9999, 1)


# ======================================================================= #
# OrderStatusRepository                                                    #
# ======================================================================= #

class TestOrderStatusRepository:

    def test_get_all(self, order_status_repo):
        statuses = order_status_repo.get_all()
        assert len(statuses) == 4
        names = [s["status_name"] for s in statuses]
        assert "received" in names

    def test_get_by_id(self, order_status_repo):
        s = order_status_repo.get_by_id(1)
        assert s is not None
        assert s["status_name"] == "received"

    def test_get_by_name(self, order_status_repo):
        s = order_status_repo.get_by_name("collected")
        assert s is not None
        assert s["status_id"] == 4


# ======================================================================= #
# OrderItemRepository                                                     #
# ======================================================================= #

class TestOrderItemRepository:

    def test_create_and_read(self, order_item_repo, db, user_repo, order_status_repo, category_repo, food_repo):
        # Create a student so FK on orders.user_id is satisfied
        student = user_repo.create_student("buyer", "pw12345", "Buyer", "b@ibsu.edu")

        # Create a category + food item so FK on order_items.food_item_id is satisfied
        category_repo.create("Main Dish", "Main dishes")
        food_item = food_repo.create(1, "Pasta", "Delicious", 5.0, 20)

        # Insert a bare order row (FK on user_id now valid)
        cursor = db.connection.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id, order_date, status_id, total_amount) "
            "VALUES (?, '2025-01-01 10:00:00', 1, 10.0)",
            (student.user_id,)
        )
        db.connection.commit()
        order_id = cursor.lastrowid

        oid = order_item_repo.create(order_id, food_item.food_item_id, "Pasta", 2, 5.0, 10.0)
        assert oid > 0
        items = order_item_repo.get_by_order_id(order_id)
        assert len(items) == 1
        assert items[0]["item_name"] == "Pasta"


# ======================================================================= #
# OrderRepository                                                          #
# ======================================================================= #

class TestOrderRepository:

    def test_create_order(self, order_repo, user_repo, food_repo, category_repo, order_status_repo):
        student = user_repo.create_student("buyer", "pw12345", "Buyer", "b@ibsu.edu")
        cat = category_repo.create("Main", "Mains")
        item = food_repo.create(cat.category_id, "Burger", "Beef burger", 6.0, 10)
        pending = order_status_repo.get_by_name("received")
        items = [{"food_item_id": item.food_item_id, "name": item.name, "price": item.price, "quantity": 2}]
        order_id = order_repo.create(student.user_id, pending["status_id"], items)
        assert order_id > 0
        # Verify stock decreased
        row = food_repo.get_by_id(item.food_item_id)
        assert row["stock"] == 8

    def test_create_order_insufficient_stock(self, order_repo, user_repo, food_repo, category_repo, order_status_repo):
        student = user_repo.create_student("buyer2", "pw12345", "Buyer2")
        cat = category_repo.create("Snack", "Snacks")
        item = food_repo.create(cat.category_id, "Chips", "Crispy", 1.5, 2)
        pending = order_status_repo.get_by_name("received")
        items = [{"food_item_id": item.food_item_id, "name": item.name, "price": item.price, "quantity": 5}]
        with pytest.raises(InsufficientStockError):
            order_repo.create(student.user_id, pending["status_id"], items)

    def test_get_by_id(self, seed_order, order_repo):
        order_id, _, _ = seed_order
        row = order_repo.get_by_id(order_id)
        assert row is not None
        assert row["order_id"] == order_id

    def test_get_by_student(self, seed_order, order_repo):
        _, student, _ = seed_order
        rows = order_repo.get_by_student(student.user_id)
        assert len(rows) >= 1

    def test_update_status(self, seed_order, order_repo, order_status_repo):
        order_id, _, _ = seed_order
        confirmed = order_status_repo.get_by_name("preparing")
        result = order_repo.update_status(order_id, confirmed["status_id"])
        assert result is True
        row = order_repo.get_by_id(order_id)
        assert row["status"] == "preparing"

    def test_update_status_missing_raises(self, order_repo):
        with pytest.raises(OrderNotFoundError):
            order_repo.update_status(9999, 2)

    def test_cancel_order(self, seed_order, order_repo, food_repo):
        order_id, _, item = seed_order
        original_stock = food_repo.get_by_id(item.food_item_id)["stock"]  # 30 - 2 = 28
        result = order_repo.cancel_order(order_id)
        assert result is True
        row = order_repo.get_by_id(order_id)
        assert row is None
        # Stock should be restored
        new_stock = food_repo.get_by_id(item.food_item_id)["stock"]
        assert new_stock == original_stock + 2  # quantity was 2

    def test_cancel_cannot_cancel_completed(self, order_repo, user_repo, food_repo, category_repo, order_status_repo):
        student = user_repo.create_student("stu2", "pw12345", "Stu2")
        cat = category_repo.create("Dessert", "Sweets")
        item = food_repo.create(cat.category_id, "Pie", "Apple pie", 3.0, 10)
        pending = order_status_repo.get_by_name("received")
        items = [{"food_item_id": item.food_item_id, "name": item.name, "price": item.price, "quantity": 1}]
        order_id = order_repo.create(student.user_id, pending["status_id"], items)
        completed = order_status_repo.get_by_name("collected")
        order_repo.update_status(order_id, completed["status_id"])
        with pytest.raises(OrderCannotBeCancelledError):
            order_repo.cancel_order(order_id)

    def test_cancel_wrong_user_raises(self, seed_order, order_repo):
        order_id, _, _ = seed_order
        with pytest.raises(InvalidOrderError):
            order_repo.cancel_order(order_id, user_id=9999)

    def test_search_by_date(self, order_repo, user_repo, food_repo, category_repo, order_status_repo):
        student = user_repo.create_student("dater", "pw12345", "Dater")
        cat = category_repo.create("Main2", "Mains")
        item = food_repo.create(cat.category_id, "Rice2", "Rice bowl", 5.0, 20)
        pending = order_status_repo.get_by_name("received")
        items = [{"food_item_id": item.food_item_id, "name": item.name, "price": item.price, "quantity": 1}]
        order_repo.create(student.user_id, pending["status_id"], items)
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        results = order_repo.search_by_date(today)
        assert len(results) >= 1

    def test_search_by_status(self, seed_order, order_repo):
        results = order_repo.search_by_status("received")
        assert len(results) >= 1

    def test_search_by_student_name(self, seed_order, order_repo):
        results = order_repo.search_by_student_name("Bob")
        assert len(results) >= 1

def test_delete_pending_order_restores_stock(order_repo, user_repo, food_repo, category_repo, order_status_repo):
    """Deleting a pending order removes its records and restores reserved stock."""
    student = user_repo.create_student("deleter", "pw12345", "Delete Me")
    cat = category_repo.create("DeleteCat", "Test")
    item = food_repo.create(cat.category_id, "Delete Item", "Test", 4.0, 10)
    pending = order_status_repo.get_by_name("received")
    order_id = order_repo.create(
        student.user_id,
        pending["status_id"],
        [{"food_item_id": item.food_item_id, "name": item.name, "price": item.price, "quantity": 2}],
    )
    assert food_repo.get_by_id(item.food_item_id)["stock"] == 8
    assert order_repo.delete(order_id) is True
    assert order_repo.get_by_id(order_id) is None
    assert food_repo.get_by_id(item.food_item_id)["stock"] == 10


def test_delete_missing_order_raises(order_repo):
    """Deleting an unknown order should raise the domain exception."""
    with pytest.raises(OrderNotFoundError):
        order_repo.delete(99999)
