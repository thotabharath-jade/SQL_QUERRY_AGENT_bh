"""
Database Setup Script
Creates the MySQL database and runs migrations.

Usage:
    python setup_database.py
"""
import pymysql
from sqlalchemy import create_engine, text
import sys
import os

# Database connection settings
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = input("Enter your MySQL root password: ")
DATABASE_NAME = "sql_agent_db"

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings


def create_database():
    """Create the database if it doesn't exist"""
    print(f"Connecting to MySQL at {MYSQL_HOST}:{MYSQL_PORT}...")
    
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{DATABASE_NAME}' created or already exists.")
        
        connection.close()
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"Error connecting to MySQL: {e}")
        print("\nPlease make sure:")
        print("1. MySQL server is running")
        print("2. You have entered the correct password")
        print("3. MySQL is accessible at the specified host/port")
        return False


def run_migrations():
    """Run Alembic migrations"""
    print("\nRunning Alembic migrations...")
    
    try:
        from alembic.config import Config
        from alembic import command
        
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error running migrations: {e}")
        return False


def verify_data():
    """Verify that seed data was inserted"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) FROM departments")).scalar()
        print(f"\nVerification: {result} departments found in database")
        
        result = db.execute(text("SELECT COUNT(*) FROM employees")).scalar()
        print(f"Verification: {result} employees found in database")
        
        result = db.execute(text("SELECT COUNT(*) FROM products")).scalar()
        print(f"Verification: {result} products found in database")
        
        result = db.execute(text("SELECT COUNT(*) FROM orders")).scalar()
        print(f"Verification: {result} orders found in database")
        
        return True
        
    except Exception as e:
        print(f"Error verifying data: {e}")
        return False
    finally:
        db.close()


def main():
    print("=" * 50)
    print("SQL Query Builder Agent - Database Setup")
    print("=" * 50)
    
    # Update DATABASE_URL in settings
    global settings
    settings.DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE_NAME}"
    
    # Step 1: Create database
    if not create_database():
        sys.exit(1)
    
    # Step 2: Run migrations
    if not run_migrations():
        sys.exit(1)
    
    # Step 3: Verify
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Update .env file with your settings")
    print("2. Start the server: uvicorn app.main:app --reload")
    print("3. Visit http://localhost:8000/docs for API documentation")


if __name__ == "__main__":
    main()
