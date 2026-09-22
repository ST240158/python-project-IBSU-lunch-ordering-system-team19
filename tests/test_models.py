"""Unit tests for domain model classes.

Covers:
  - Property validation (setters rejecting bad values)
  - Dunder methods (__str__, __repr__, __eq__, __hash__, __len__, __contains__)
  - Abstract method enforcement (User cannot be instantiated)
  - Polymorphism (Student vs Administrator override behaviour)
  - Composition (Order contains OrderItem; FoodItem belongs to Category)
  - Computed properties (OrderItem.subtotal, Order.computed_total)
"""

import pytest

from src.models.user import User
from src.models.student import Student
from src.models.administrator import Administrator
from src.models.category import Category
from src.models.food_item import FoodItem
from src.models.order_item import OrderItem
from src.models.order import Order
from src.models.order_status import OrderStatus


# ======================================================================= #
# User (ABC) — abstract enforcement                                         #
# ======================================================================= #

class TestUserABC:
    """User is abstract; it must not be instantiated directly."""

    def test_cannot_instantiate_user(self):
        with pytest.raises(TypeError):
            User(user_id=1, username="abc", password_hash="hash", role="student")

    def test_subclass_student_instantiates(self):
        s = Student(user_id=1, username="alice", name="Alice")
        assert s.role == "student"

    def test_subclass_admin_instantiates(self):
        a = Administrator(user_id=2, username="bob", name="Bob")
        assert a.role == "admin"


# ======================================================================= #
# User property validation                                                  #
# ======================================================================= #

class TestUserProperties:

    def test_user_id_negative_raises(self):
        s = Student()
        with pytest.raises(ValueError):
            s.user_id = -1

    def test_user_id_non_int_raises(self):
        s = Student()
        with pytest.raises(ValueError):
            s.user_id = "abc"  # type: ignore[assignment]

    def test_username_too_short(self):
        s = Student()
        with pytest.raises(ValueError):
            s.username = "ab"

    def test_username_valid(self):
        s = Student()
        s.username = "valid_user"
        assert s.username == "valid_user"

    def test_password_hash_empty_raises(self):
        s = Student()
        with pytest.raises(ValueError):
            s.password_hash = ""

    def test_role_invalid_raises(self):
        s = Student()
        with pytest.raises(ValueError):
            s.role = "manager"


# ======================================================================= #
# Student                                                                   #
# ======================================================================= #

class TestStudent:

    def test_default_role_is_student(self):
        s = Student()
        assert s.role == "student"

    def test_name_property(self):
        s = Student(name="  Alice  ")
        assert s.name == "Alice"

    def test_name_empty_raises(self):
        s = Student()
        with pytest.raises(ValueError):
            s.name = ""

    def test_contact_info_property(self):
        s = Student(contact_info="  alice@ibsu.edu  ")
        assert s.contact_info == "alice@ibsu.edu"

    def test_get_menu_options(self):
        s = Student()
        opts = s.get_menu_options()
        assert "Place Order" in opts
        assert "Logout" in opts

    def test_cannot_manage_menu(self):
        s = Student()
        assert s.can_manage_menu() is False

    def test_cannot_update_order_status(self):
        s = Student()
        assert s.can_update_order_status() is False

    def test_str(self):
        s = Student(user_id=5, username="alice", name="Alice")
        assert "alice" in str(s)
        assert "Alice" in str(s)

    def test_repr(self):
        s = Student(user_id=5, username="alice")
        assert "Student" in repr(s)

    def test_eq_same_id(self):
        a = Student(user_id=1)
        b = Student(user_id=1)
        assert a == b

    def test_eq_different_id(self):
        a = Student(user_id=1)
        b = Student(user_id=2)
        assert a != b

    def test_eq_not_student(self):
        a = Student(user_id=1)
        assert a != 42

    def test_hash(self):
        a = Student(user_id=1)
        b = Student(user_id=1)
        assert hash(a) == hash(b)


# ======================================================================= #
# Administrator                                                             #
# ======================================================================= #

class TestAdministrator:

    def test_default_role_is_admin(self):
        a = Administrator()
        assert a.role == "admin"

    def test_name_property(self):
        a = Administrator(name="  Admin  ")
        assert a.name == "Admin"

    def test_name_empty_raises(self):
        a = Administrator()
        with pytest.raises(ValueError):
            a.name = ""

    def test_get_menu_options(self):
        a = Administrator()
        opts = a.get_menu_options()
        assert "Add Food Item" in opts
        assert "Logout" in opts

    def test_can_manage_menu(self):
        a = Administrator()
        assert a.can_manage_menu() is True

    def test_can_update_order_status(self):
        a = Administrator()
        assert a.can_update_order_status() is True

    def test_str(self):
        a = Administrator(user_id=1, username="admin", name="Admin")
        assert "admin" in str(a)

    def test_eq(self):
        a = Administrator(user_id=1)
        b = Administrator(user_id=1)
        assert a == b


# ======================================================================= #
# Polymorphism — Student vs Administrator                                  #
# ======================================================================= #

class TestPolymorphism:

    def test_menu_options_differ(self):
        s = Student()
        a = Administrator()
        assert s.get_menu_options() != a.get_menu_options()

    def test_permissions_differ(self):
        s = Student()
        a = Administrator()
        assert s.can_manage_menu() != a.can_manage_menu()
        assert s.can_update_order_status() != a.can_update_order_status()


# ======================================================================= #
# Category                                                                  #
# ======================================================================= #

class TestCategory:

    def test_create_defaults(self):
        c = Category()
        assert c.category_id == 0
        assert c.category_name == ""

    def test_category_name_empty_raises(self):
        c = Category()
        with pytest.raises(ValueError):
            c.category_name = ""

    def test_category_name_valid(self):
        c = Category(category_name="  Main Dish  ")
        assert c.category_name == "Main Dish"

    def test_category_id_negative_raises(self):
        c = Category()
        with pytest.raises(ValueError):
            c.category_id = -5

    def test_description_stripped(self):
        c = Category(description="  yummy  ")
        assert c.description == "yummy"

    def test_str(self):
        c = Category(category_id=1, category_name="Beverage")
        assert "Beverage" in str(c)

    def test_repr(self):
        c = Category(category_id=1, category_name="Beverage")
        assert "Category" in repr(c)

    def test_eq(self):
        a = Category(category_id=1)
        b = Category(category_id=1)
        assert a == b

    def test_hash(self):
        a = Category(category_id=1)
        b = Category(category_id=1)
        assert hash(a) == hash(b)


# ======================================================================= #
# FoodItem                                                                  #
# ======================================================================= #

class TestFoodItem:

    def test_price_negative_raises(self):
        f = FoodItem()
        with pytest.raises(ValueError):
            f.price = -1.0

    def test_price_rounded(self):
        f = FoodItem()
        f.price = 3.456
        assert f.price == 3.46

    def test_stock_negative_raises(self):
        f = FoodItem()
        with pytest.raises(ValueError):
            f.stock = -1

    def test_name_empty_raises(self):
        f = FoodItem()
        with pytest.raises(ValueError):
            f.name = ""

    def test_name_stripped(self):
        f = FoodItem(name="  Pasta  ")
        assert f.name == "Pasta"

    def test_composition_category(self):
        """FoodItem holds category_id — composition relationship."""
        f = FoodItem(category_id=3, category_name="Beverage")
        assert f.category_id == 3
        assert f.category_name == "Beverage"

    def test_str(self):
        f = FoodItem(food_item_id=10, name="Coffee", price=2.0, stock=50)
        assert "Coffee" in str(f)

    def test_repr(self):
        f = FoodItem(food_item_id=10, name="Coffee")
        assert "FoodItem" in repr(f)

    def test_eq(self):
        a = FoodItem(food_item_id=1)
        b = FoodItem(food_item_id=1)
        assert a == b


# ======================================================================= #
# OrderItem                                                                 #
# ======================================================================= #

class TestOrderItem:

    def test_quantity_zero_raises(self):
        oi = OrderItem()
        with pytest.raises(ValueError):
            oi.quantity = 0

    def test_quantity_negative_raises(self):
        oi = OrderItem()
        with pytest.raises(ValueError):
            oi.quantity = -2

    def test_subtotal_computed(self):
        oi = OrderItem(quantity=3, unit_price=5.50)
        assert oi.subtotal == 16.50

    def test_unit_price_negative_raises(self):
        oi = OrderItem()
        with pytest.raises(ValueError):
            oi.unit_price = -1.0

    def test_str(self):
        oi = OrderItem(item_name="Cake", quantity=2, unit_price=4.0)
        assert "Cake" in str(oi)

    def test_eq(self):
        a = OrderItem(order_item_id=1)
        b = OrderItem(order_item_id=1)
        assert a == b


# ======================================================================= #
# Order — composition with OrderItem                                        #
# ======================================================================= #

class TestOrder:

    def test_default_status(self):
        o = Order()
        assert o.status == "received"

    def test_invalid_status_raises(self):
        o = Order()
        with pytest.raises(ValueError):
            o.status = "Cooking"

    def test_add_item_composition(self):
        o = Order()
        oi = OrderItem(item_name="Tea", quantity=1, unit_price=2.0)
        o.add_item(oi)
        assert len(o.items) == 1

    def test_add_non_orderitem_raises(self):
        o = Order()
        with pytest.raises(TypeError):
            o.add_item("not an item")  # type: ignore[arg-type]

    def test_remove_item(self):
        o = Order()
        oi = OrderItem(food_item_id=10, item_name="Tea", quantity=1, unit_price=2.0)
        o.add_item(oi)
        o.remove_item(10)
        assert len(o.items) == 0

    def test_computed_total(self):
        o = Order()
        o.add_item(OrderItem(quantity=2, unit_price=5.0))   # 10.00
        o.add_item(OrderItem(quantity=1, unit_price=3.50))   #  3.50
        assert o.computed_total == 13.50

    def test_len_dunder(self):
        o = Order()
        o.add_item(OrderItem())
        o.add_item(OrderItem())
        assert len(o) == 2

    def test_contains_dunder(self):
        o = Order()
        oi = OrderItem(order_item_id=42)
        o.add_item(oi)
        assert oi in o

    def test_total_negative_raises(self):
        o = Order()
        with pytest.raises(ValueError):
            o.total_amount = -1.0

    def test_str(self):
        o = Order(order_id=1, student_name="Alice")
        assert "Alice" in str(o)

    def test_eq(self):
        a = Order(order_id=1)
        b = Order(order_id=1)
        assert a == b

    def test_hash(self):
        a = Order(order_id=1)
        b = Order(order_id=1)
        assert hash(a) == hash(b)


# ======================================================================= #
# OrderStatus                                                               #
# ======================================================================= #

class TestOrderStatus:

    def test_valid_status(self):
        os = OrderStatus(status_id=1, status_name="received")
        assert os.status_name == "received"

    def test_invalid_status_raises(self):
        os = OrderStatus()
        with pytest.raises(ValueError):
            os.status_name = "Delivered"

    def test_str(self):
        os = OrderStatus(status_id=3, status_name="preparing")
        assert "preparing" in str(os)

    def test_eq(self):
        a = OrderStatus(status_id=1)
        b = OrderStatus(status_id=1)
        assert a == b