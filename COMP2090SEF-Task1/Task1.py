# Campus Second-hand Trading Platform (Group9)
# No Conda required, runs directly in any Python 3 environment (Trae included)
# Core OOP implementation (Python Class, ADT, Modular Programming)
from abc import ABC, abstractmethod

# ------------------------------
# 1. Abstract Data Type (ADT) for Users
# ------------------------------
class BaseUser(ABC):
    """Abstract base class for all platform users (ADT)
    Enforces essential methods for all user types
    """
    @abstractmethod
    def get_info(self):
        """Must return user's basic information"""
        pass

    @abstractmethod
    def change_email(self, new_email):
        """Must handle email updates with validation"""
        pass

# ------------------------------
# 2. Core User Classes (Inheritance + Encapsulation)
# ------------------------------
class User(BaseUser):
    """Basic user class (implements BaseUser ADT)"""
    def __init__(self, name, user_id, email):
        # Encapsulation: Private attributes (only accessible via methods)
        self._name = name  # Protected (simplified for student-level code)
        self._id = user_id
        self._email = email

    def get_info(self):
        """Implement abstract method - return user info"""
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email
        }

    def change_email(self, new_email):
        """Implement abstract method - update email (campus domain check)"""
        if "@school.edu" in new_email:
            self._email = new_email
            print(f"  ✓ Email updated for {self._name}: {new_email}")
            return True
        print(f"  ✗ Error: {new_email} is not a valid campus email")
        return False

    def __str__(self):
        """Human-readable user info"""
        return f"User({self._id}): {self._name}"

class Seller(User):
    """Seller subclass (inherits from User)"""
    def __init__(self, name, user_id, email, store):
        super().__init__(name, user_id, email)
        self.store_name = store  # Seller-specific attribute

    # Polymorphism: Override parent method
    def get_info(self):
        basic_info = super().get_info()
        basic_info["store"] = self.store_name
        return basic_info

class Buyer(User):
    """Buyer subclass (inherits from User)"""
    def __init__(self, name, user_id, email, address):
        super().__init__(name, user_id, email)
        self.shipping_addr = address  # Buyer-specific attribute

    # Polymorphism: Override parent method
    def get_info(self):
        basic_info = super().get_info()
        basic_info["shipping_address"] = self.shipping_addr
        return basic_info

# ------------------------------
# 3. Product & Order Classes (Encapsulation)
# ------------------------------
class Book:
    """Second-hand book class (ADT for product)"""
    def __init__(self, book_id, title, author, seller_id, price, condition):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.seller_id = seller_id
        self.price = self._check_price(price)
        self.condition = condition  # "new", "like_new", "used", "sold"

    # Simple validation (private helper)
    def _check_price(self, price):
        if price < 0:
            raise ValueError("Price can't be negative!")
        return round(price, 1)

    def update_condition(self, new_cond):
        """Update book condition with validation"""
        valid_conds = ["new", "like_new", "used", "sold"]
        if new_cond in valid_conds:
            self.condition = new_cond
            print(f"  ✓ Book {self.book_id} condition: {new_cond}")
            return True
        print(f"  ✗ Invalid condition. Choose: {valid_conds}")
        return False

    def get_book_details(self):
        """Return book info (encapsulated access)"""
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "seller": self.seller_id,
            "price": self.price,
            "condition": self.condition
        }

class Order:
    """Order class (ADT for transactions)"""
    def __init__(self, order_id, buyer_id, book_id, total):
        self.order_id = order_id
        self.buyer_id = buyer_id
        self.book_id = book_id
        self.total = self._check_price(total)
        self.status = "pending"  # Default status

    def _check_price(self, price):
        if price < 0:
            raise ValueError("Order total can't be negative!")
        return round(price, 1)

    def update_status(self, new_status):
        """Update order status (pending/paid/shipped/completed/cancelled)"""
        valid_statuses = ["pending", "paid", "shipped", "completed", "cancelled"]
        if new_status in valid_statuses:
            self.status = new_status
            print(f"  ✓ Order {self.order_id} status: {new_status}")
            return True
        print(f"  ✗ Invalid status. Choose: {valid_statuses}")
        return False

    def get_order_details(self):
        """Return order info"""
        return {
            "id": self.order_id,
            "buyer": self.buyer_id,
            "book": self.book_id,
            "total": self.total,
            "status": self.status
        }

# ------------------------------
# 4. Modular Data Managers (Separation of Concerns)
# ------------------------------
class DataHandler:
    """Basic data manager (reusable for all data types)"""
    def __init__(self):
        self.items = []  # Store all items (users/books/orders)

    def add(self, item):
        """Add item (prevent duplicate IDs)"""
        try:
            # Check duplicates based on item type
            if hasattr(item, "get_info"):
                item_id = item.get_info()["id"]
                for i in self.items:
                    if i.get_info()["id"] == item_id:
                        raise ValueError(f"User {item_id} already exists")
            elif hasattr(item, "get_book_details"):
                item_id = item.book_id
                for i in self.items:
                    if hasattr(i, "book_id") and i.book_id == item_id:
                        raise ValueError(f"Book {item_id} already exists")
            elif hasattr(item, "get_order_details"):
                item_id = item.order_id
                for i in self.items:
                    if hasattr(i, "order_id") and i.order_id == item_id:
                        raise ValueError(f"Order {item_id} already exists")
            
            self.items.append(item)
            print(f"  ➕ Added {item_id} successfully")
            return True
        except ValueError as e:
            print(f"  ✗ Add failed: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            return False

    def remove(self, item_id):
        """Remove item by ID"""
        for idx, item in enumerate(self.items):
            if hasattr(item, "get_info") and item.get_info()["id"] == item_id:
                del self.items[idx]
                print(f"  🗑️ Removed user {item_id}")
                return True
            elif hasattr(item, "book_id") and item.book_id == item_id:
                del self.items[idx]
                print(f"  🗑️ Removed book {item_id}")
                return True
            elif hasattr(item, "order_id") and item.order_id == item_id:
                del self.items[idx]
                print(f"  🗑️ Removed order {item_id}")
                return True
        print(f"  ✗ Item {item_id} not found")
        return False

    def get_all(self):
        """Return all stored items"""
        return self.items

# Specialized managers (modular, single responsibility)
class UserHandler(DataHandler):
    """Manage user data only"""
    pass

class BookHandler(DataHandler):
    """Manage book data only"""
    pass

class OrderHandler(DataHandler):
    """Manage order data only"""
    pass

# ------------------------------
# 5. Test Code (Clean formatting, English output)
# ------------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print("          CAMPUS SECOND-HAND TRADING PLATFORM TEST")
    print("="*60)

    # Initialize managers
    user_manager = UserHandler()
    book_manager = BookHandler()
    order_manager = OrderHandler()

    # 1. Create users
    print("\n[1] CREATE USERS")
    seller_1 = Seller("Anna", "S001", "anna@school.edu", "Anna's Book Shop")
    buyer_1 = Buyer("Ben", "B001", "ben@school.edu", "Dorm 5, Room 102")
    user_manager.add(seller_1)
    user_manager.add(buyer_1)

    # 2. Display user info (polymorphism)
    print("\n[2] USER INFORMATION (POLYMORPHISM)")
    print("  Seller info:", seller_1.get_info())
    print("  Buyer info:", buyer_1.get_info())

    # 3. Create product and order
    print("\n[3] CREATE PRODUCT & ORDER")
    try:
        book_1 = Book("BK001", "Python Basics", "John Smith", "S001", 19.9, "like_new")
        book_manager.add(book_1)
    except ValueError as e:
        print(f"  ✗ Book creation failed: {e}")

    try:
        order_1 = Order("OD001", "B001", "BK001", 19.9)
        order_manager.add(order_1)
    except ValueError as e:
        print(f"  ✗ Order creation failed: {e}")

    # 4. Update statuses
    print("\n[4] STATUS UPDATES")
    book_1.update_condition("sold")
    order_1.update_status("paid")
    buyer_1.change_email("ben_new@school.edu")

    # 5. Data summary (categorized)
    print("\n" + "-"*60)
    print("[5] PLATFORM DATA SUMMARY")
    print("-"*60)

    # Seller information
    print("\n1. Sellers")
    sellers = [u for u in user_manager.get_all() if isinstance(u, Seller)]
    if sellers:
        for s in sellers:
            info = s.get_info()
            print(f"   - ID: {info['id']}, Name: {info['name']}, Email: {info['email']}, Store: {info['store']}")
    else:
        print("   No sellers")

    # Buyer information
    print("\n2. Buyers")
    buyers = [u for u in user_manager.get_all() if isinstance(u, Buyer)]
    if buyers:
        for b in buyers:
            info = b.get_info()
            print(f"   - ID: {info['id']}, Name: {info['name']}, Email: {info['email']}, Shipping: {info['shipping_address']}")
    else:
        print("   No buyers")

    # Books information
    print("\n3. Books")
    books = book_manager.get_all()
    if books:
        for b in books:
            details = b.get_book_details()
            print(f"   - ID: {details['id']}, Title: {details['title']}, Author: {details['author']}, "
                  f"Seller: {details['seller']}, Price: {details['price']}, Condition: {details['condition']}")
    else:
        print("   No books")

    # Orders information
    print("\n4. Orders")
    orders = order_manager.get_all()
    if orders:
        for o in orders:
            details = o.get_order_details()
            print(f"   - Order ID: {details['id']}, Buyer: {details['buyer']}, Book: {details['book']}, "
                  f"Total: {details['total']}, Status: {details['status']}")
    else:
        print("   No orders")

    # 6. Remove test
    print("\n" + "-"*60)
    print("[6] REMOVE TEST")
    book_manager.remove("BK001")

    print("\n" + "="*60)
    print("                  TEST COMPLETED")
    print("="*60 + "\n")