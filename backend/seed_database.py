"""
Manual seed script for the database.
Run this after migrations to populate sample data.

Usage:
    python seed_database.py
"""
import pymysql
from sqlalchemy import text
from sqlalchemy.engine import make_url
from app.core.database import SessionLocal, engine, Base
from app.core.config import settings

# Import all models so SQLAlchemy knows about them
from app.models.seed_data import Department, Employee, Product, Order


def ensure_database_exists():
    """Create the target database if it doesn't exist."""
    url = make_url(settings.DATABASE_URL)
    database_name = url.database
    if not database_name:
        raise ValueError("DATABASE_URL must include a database name")

    print(f"Ensuring database '{database_name}' exists...")

    # pymysql connect to server (without database)
    tmp_connection = pymysql.connect(
        host=url.host or "localhost",
        port=url.port or 3306,
        user=url.username or "root",
        password=url.password or "",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

    try:
        with tmp_connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print(f"Database '{database_name}' is ready.")
    finally:
        tmp_connection.close()


def seed_departments(db):
    departments = [
        ("Engineering", "Building A"),
        ("Marketing", "Building B"),
        ("Sales", "Building C"),
        ("Human Resources", "Building A"),
        ("Finance", "Building D"),
    ]
    for name, location in departments:
        db.execute(text(
            "INSERT INTO departments (name, location) VALUES (:name, :location)"
        ), {"name": name, "location": location})
    print(f"Inserted {len(departments)} departments")


def seed_employees(db):
    employees = [
        ("Alice Johnson", "alice@company.com", 1, 85000.00),
        ("Bob Smith", "bob@company.com", 1, 92000.00),
        ("Charlie Brown", "charlie@company.com", 2, 65000.00),
        ("Diana Prince", "diana@company.com", 3, 70000.00),
        ("Eve Wilson", "eve@company.com", 4, 55000.00),
        ("Frank Miller", "frank@company.com", 5, 78000.00),
        ("Grace Lee", "grace@company.com", 1, 105000.00),
        ("Henry Davis", "henry@company.com", 3, 62000.00),
        ("Ivy Chen", "ivy@company.com", 2, 58000.00),
        ("Jack Taylor", "jack@company.com", 1, 88000.00),
    ]
    for name, email, dept_id, salary in employees:
        db.execute(text(
            "INSERT INTO employees (name, email, dept_id, salary, hire_date) VALUES (:name, :email, :dept_id, :salary, NOW())"
        ), {"name": name, "email": email, "dept_id": dept_id, "salary": salary})
    print(f"Inserted {len(employees)} employees")


def seed_products(db):
    products = [
        ("Laptop Pro 15", "Electronics", 1299.99, 50),
        ("Wireless Mouse", "Electronics", 29.99, 200),
        ("USB-C Cable", "Accessories", 12.99, 500),
        ("Mechanical Keyboard", "Electronics", 89.99, 75),
        ("Monitor 27 inch", "Electronics", 349.99, 30),
        ("Desk Chair", "Furniture", 199.99, 45),
        ("Desk Lamp", "Furniture", 34.99, 100),
        ("Webcam HD", "Electronics", 79.99, 80),
        ("Headphones Wireless", "Electronics", 149.99, 120),
        ("External SSD 1TB", "Electronics", 109.99, 60),
    ]
    for name, category, price, stock in products:
        db.execute(text(
            "INSERT INTO products (name, category, price, stock_quantity) VALUES (:name, :category, :price, :stock)"
        ), {"name": name, "category": category, "price": price, "stock": stock})
    print(f"Inserted {len(products)} products")


def seed_orders(db):
    orders = [
        ("John Customer", 1, 1, 1299.99, "completed"),
        ("Sarah Buyer", 2, 3, 89.97, "completed"),
        ("Mike Purchaser", 4, 1, 89.99, "shipped"),
        ("Emily Shopper", 5, 2, 699.98, "pending"),
        ("David Client", 9, 1, 149.99, "completed"),
        ("Lisa Customer", 3, 5, 64.95, "shipped"),
        ("Robert Buyer", 6, 2, 399.98, "pending"),
        ("Jennifer Shopper", 10, 1, 109.99, "completed"),
        ("Thomas Client", 7, 3, 104.97, "shipped"),
        ("Amanda Purchaser", 8, 2, 159.98, "completed"),
    ]
    for customer, product_id, quantity, total, status in orders:
        db.execute(text(
            "INSERT INTO orders (customer_name, product_id, quantity, total_amount, order_date, status) VALUES (:customer, :product_id, :quantity, :total, NOW(), :status)"
        ), {"customer": customer, "product_id": product_id, "quantity": quantity, "total": total, "status": status})
    print(f"Inserted {len(orders)} orders")


def create_tables():
    """Create all tables if they don't exist."""
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


def main():
    ensure_database_exists()
    create_tables()

    db = SessionLocal()
    try:
        print("Starting database seeding...")
        seed_departments(db)
        seed_employees(db)
        seed_products(db)
        seed_orders(db)
        db.commit()
        print("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
