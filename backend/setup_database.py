"""
Database Setup Script
Creates both MySQL databases (sqlquerrydb and sql_agent_db) and runs migrations.

Usage:
    python setup_database.py
"""
import pymysql
from sqlalchemy import create_engine, text
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings


def get_sync_url(async_url: str) -> str:
    """Convert async URL to sync URL."""
    return async_url.replace("+aiomysql", "+pymysql")


def create_database(db_url: str, label: str):
    """Create a database if it doesn't exist"""
    from sqlalchemy.engine import make_url
    url = make_url(get_sync_url(db_url))
    database_name = url.database

    print(f"Creating {label} database '{database_name}'...")

    try:
        connection = pymysql.connect(
            host=url.host or "localhost",
            port=url.port or 3306,
            user=url.username or "root",
            password=url.password or "",
            charset='utf8mb4'
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print(f"  '{database_name}' is ready.")

        connection.close()
        return True

    except pymysql.err.OperationalError as e:
        print(f"Error connecting to MySQL: {e}")
        print("\nPlease make sure:")
        print("1. MySQL server is running")
        print("2. Credentials in .env are correct")
        return False


def run_migrations():
    """Run Alembic migrations for the app database"""
    print("\nRunning Alembic migrations on sqlquerrydb...")

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


def main():
    print("=" * 50)
    print("SQL Query Builder Agent - Database Setup")
    print("=" * 50)

    # Step 1: Create app database (sqlquerrydb)
    if not create_database(settings.APP_DATABASE_URL, "App"):
        sys.exit(1)

    # Step 2: Create default target database (sql_agent_db)
    if not create_database(settings.DEFAULT_TARGET_DB_URL, "Default Target"):
        sys.exit(1)

    # Step 3: Run Alembic migrations (on sqlquerrydb)
    if not run_migrations():
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Run: python seed_database.py   (to populate sample data)")
    print("2. Run: uvicorn app.main:app --reload")
    print("3. Visit http://localhost:8000/docs for API documentation")


if __name__ == "__main__":
    main()
