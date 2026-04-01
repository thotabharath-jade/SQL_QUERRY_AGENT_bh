# SQL Query Builder Agent - Backend

## Setup Instructions


### 1. Database Setup

#### a. LLM/SQL Database (MySQL)
1. Open MySQL Workbench and connect to your local MySQL server
2. Create a new database:
```sql
CREATE DATABASE sql_agent_db;
```

#### b. User Authentication Database (SQLite by default)
No setup required for SQLite (default: `auth_db.sqlite3` in backend directory). You can change `AUTH_DATABASE_URL` in `app/core/config.py` to use another RDBMS if desired.

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


# Copy and edit environment file
cp .env.example .env
# Edit .env with your MySQL credentials and OpenAI API key
# Optionally, set `AUTH_DATABASE_URL` for user profile storage (default is SQLite)


# Run migrations (for LLM/SQL DB only)
alembic upgrade head

# User authentication DB tables are auto-created on first run if using SQLite. For other DBs, create tables using `init_auth_db()` in `app/core/database.py`.

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints


### Authentication (Separate DB)
- `POST /api/auth/register` - Register new user (stored in auth DB)
- `POST /api/auth/login` - Login (returns JWT token, checks auth DB)
- `GET /api/auth/me` - Get current user info (from auth DB)

> **Note:** User profile and authentication data is stored in a dedicated database, separate from the LLM/SQL database. This allows the LLM/SQL database to be changed per user/session without affecting user accounts.

### Query
- `GET /api/query/schema` - Get database schema
- `POST /api/query/execute` - Execute a natural language query

### History
- `GET /api/history/` - Get query history
- `GET /api/history/bookmarked` - Get bookmarked queries
- `POST /api/history/{id}/bookmark` - Toggle bookmark

## Alembic Commands

```bash
# Create new migration
alembic revision -m "description"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show current revision
alembic current
```
