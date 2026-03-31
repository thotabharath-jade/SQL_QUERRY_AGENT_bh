"""seed data

Revision ID: 002_seed_data
Revises: 001_initial
Create Date: 2026-03-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_seed_data'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Seed Departments
    op.execute("""
        INSERT INTO departments (name, location) VALUES
        ('Engineering', 'Building A'),
        ('Marketing', 'Building B'),
        ('Sales', 'Building C'),
        ('Human Resources', 'Building A'),
        ('Finance', 'Building D')
    """)

    # Seed Employees
    op.execute("""
        INSERT INTO employees (name, email, dept_id, salary, hire_date) VALUES
        ('Alice Johnson', 'alice@company.com', 1, 85000.00, '2022-03-15 09:00:00'),
        ('Bob Smith', 'bob@company.com', 1, 92000.00, '2021-08-20 09:00:00'),
        ('Charlie Brown', 'charlie@company.com', 2, 65000.00, '2023-01-10 09:00:00'),
        ('Diana Prince', 'diana@company.com', 3, 70000.00, '2022-06-01 09:00:00'),
        ('Eve Wilson', 'eve@company.com', 4, 55000.00, '2020-11-25 09:00:00'),
        ('Frank Miller', 'frank@company.com', 5, 78000.00, '2021-04-18 09:00:00'),
        ('Grace Lee', 'grace@company.com', 1, 105000.00, '2019-09-30 09:00:00'),
        ('Henry Davis', 'henry@company.com', 3, 62000.00, '2023-02-14 09:00:00'),
        ('Ivy Chen', 'ivy@company.com', 2, 58000.00, '2022-10-05 09:00:00'),
        ('Jack Taylor', 'jack@company.com', 1, 88000.00, '2021-12-01 09:00:00')
    """)

    # Seed Products
    op.execute("""
        INSERT INTO products (name, category, price, stock_quantity) VALUES
        ('Laptop Pro 15', 'Electronics', 1299.99, 50),
        ('Wireless Mouse', 'Electronics', 29.99, 200),
        ('USB-C Cable', 'Accessories', 12.99, 500),
        ('Mechanical Keyboard', 'Electronics', 89.99, 75),
        ('Monitor 27 inch', 'Electronics', 349.99, 30),
        ('Desk Chair', 'Furniture', 199.99, 45),
        ('Desk Lamp', 'Furniture', 34.99, 100),
        ('Webcam HD', 'Electronics', 79.99, 80),
        ('Headphones Wireless', 'Electronics', 149.99, 120),
        ('External SSD 1TB', 'Electronics', 109.99, 60)
    """)

    # Seed Orders
    op.execute("""
        INSERT INTO orders (customer_name, product_id, quantity, total_amount, order_date, status) VALUES
        ('John Customer', 1, 1, 1299.99, '2024-01-15 10:30:00', 'completed'),
        ('Sarah Buyer', 2, 3, 89.97, '2024-01-16 14:20:00', 'completed'),
        ('Mike Purchaser', 4, 1, 89.99, '2024-01-17 09:15:00', 'shipped'),
        ('Emily Shopper', 5, 2, 699.98, '2024-01-18 16:45:00', 'pending'),
        ('David Client', 9, 1, 149.99, '2024-01-19 11:00:00', 'completed'),
        ('Lisa Customer', 3, 5, 64.95, '2024-01-20 13:30:00', 'shipped'),
        ('Robert Buyer', 6, 2, 399.98, '2024-01-21 10:00:00', 'pending'),
        ('Jennifer Shopper', 10, 1, 109.99, '2024-01-22 15:15:00', 'completed'),
        ('Thomas Client', 7, 3, 104.97, '2024-01-23 12:00:00', 'shipped'),
        ('Amanda Purchaser', 8, 2, 159.98, '2024-01-24 14:30:00', 'completed')
    """)


def downgrade() -> None:
    op.execute("DELETE FROM orders")
    op.execute("DELETE FROM products")
    op.execute("DELETE FROM employees")
    op.execute("DELETE FROM departments")
