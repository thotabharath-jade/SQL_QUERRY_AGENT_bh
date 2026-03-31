# SQL Query Builder Agent - Backend

## Setup Instructions

### 1. Database Setup (MySQL)

1. Open MySQL Workbench and connect to your local MySQL server
2. Create a new database:
```sql
CREATE DATABASE sql_agent_db;
```

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

# Run migrations
alembic upgrade head

# Seed the database (happens automatically with migrations)
# If you need to reseed:
alembic upgrade head --sql | mysql -u root -p sql_agent_db

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (returns JWT token)
- `GET /api/auth/me` - Get current user info

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
