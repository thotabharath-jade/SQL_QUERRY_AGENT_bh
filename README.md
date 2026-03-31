# SQL Query Builder Agent

A full-stack application that converts natural language questions into SQL queries using AI.

## Project Structure

```
sql-agent/
├── backend/           # FastAPI backend
│   ├── alembic/       # Database migrations
│   ├── app/           # Main application
│   │   ├── api/       # API routes
│   │   ├── core/      # Core configuration
│   │   ├── models/    # SQLAlchemy models
│   │   └── schemas/   # Pydantic schemas
│   └── requirements.txt
└── frontend/          # React frontend (to be created)
```

## Quick Start

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup (coming soon)

```bash
cd frontend
npm install
npm run dev
```

## Database Schema

The application uses the following tables:
- `users` - User accounts
- `departments` - Company departments
- `employees` - Employee records
- `products` - Product catalog
- `orders` - Customer orders
- `query_history` - Query execution history

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic
- **Database**: MySQL 8.0
- **Frontend**: React 18, Vite, Tailwind CSS
- **AI**: OpenAI/Groq API
