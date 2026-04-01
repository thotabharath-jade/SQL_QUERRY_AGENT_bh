# SQL Query Builder Agent

An AI-powered SQL query builder that converts natural language questions into SQL queries using local LLM (Ollama).

---

## 🎯 Current Status

### ✅ Phase 1: Setup & Infrastructure - **COMPLETE**
- [x] Project structure created
- [x] MySQL database configured (`sql_agent_db`)
- [x] Alembic migrations setup
- [x] Database models defined (User, QueryHistory)
- [x] Sample data seeded (Employees, Departments, Products, Orders)

### ✅ Phase 2: Backend Core - **COMPLETE**
- [x] JWT Authentication (Login/Register)
- [x] Schema Introspection endpoint (`GET /api/query/schema`)
- [x] LLM Integration with Ollama (`POST /api/query/ask`)
- [x] SQL Query Execution with safety validation
- [x] Query History API with bookmarking

### ✅ Phase 3: Frontend Interface - **COMPLETE**
- [x] React + Vite setup
- [x] Auth pages (Login/Signup)
- [x] Main chat interface with query history sidebar
- [x] SQL display with syntax highlighting
- [x] Results table display

### ⏳ Phase 4: Advanced Features - **PENDING**
- [ ] Data visualization (Recharts integration ready)
- [ ] Suggested questions based on schema
- [ ] Error handling improvements
- [ ] Export results to CSV

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0 (running on port 3306)
- Ollama server (your configured endpoint)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment file
copy .env.example .env  # Windows
# cp .env.example .env   # Linux/Mac

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

### 2. Frontend Setup

```bash
# Navigate to frontend (in new terminal)
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at: http://localhost:3000

### 3. Test the Backend API

```bash
# Register a user
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123", "full_name": "Test User"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'

# Get database schema
curl -X GET "http://localhost:8000/api/query/schema" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Ask a question
curl -X POST "http://localhost:8000/api/query/ask" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all employees with salary greater than 50000"}'
```

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ⚙️ Configuration

### Environment Variables

Edit `backend/.env`:

```env
# Database
DATABASE_URL=mysql+pymysql://root:12345@localhost:3306/sql_agent_db

# LLM Settings (Ollama)
LLM_PROVIDER=llama
LLAMA_BASE_URL=https://aimodels.jadeglobal.com:8082/ollama/api
LLAMA_MODEL=deepseek-coder:6.7b
LLAMA_VERIFY_SSL=false

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Query Settings
MAX_QUERY_ROWS=100
QUERY_TIMEOUT_SECONDS=30
```

---

## 📊 Database Schema

### Tables Created by Migrations

| Table | Description |
|-------|-------------|
| `users` | User accounts with authentication |
| `query_history` | Stores all queries and results |

### Seeded Tables (Sample Data)

| Table | Description | Sample Columns |
|-------|-------------|----------------|
| `departments` | Company departments | id, name, location |
| `employees` | Employee records | id, name, email, department_id, salary, hire_date |
| `products` | Product catalog | id, name, category, price, stock_quantity |
| `orders` | Customer orders | id, customer_name, product_id, quantity, order_date, status |

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get token |
| GET | `/api/auth/me` | Get current user info |

### Query

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/query/schema` | Get database schema |
| POST | `/api/query/ask` | Ask question in natural language |

### History

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/history/` | Get query history |
| GET | `/api/history/{id}` | Get specific history item |
| POST | `/api/history/{id}/bookmark` | Toggle bookmark |
| DELETE | `/api/history/{id}` | Delete history item |

---

## 📁 Project Structure

```
sql-agent/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes (auth, query, history)
│   │   ├── core/             # Config, database, security
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic (LLM, query, schema)
│   │   └── main.py           # FastAPI application
│   ├── alembic/              # Database migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/            # Login, Register, Dashboard
│   │   ├── services/         # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🔮 Next Steps (Phase 4)

1. **Data Visualization**: Integrate Recharts for chart generation
2. **Suggested Questions**: Auto-generate example queries
3. **Error Handling**: Improve user-friendly error messages
4. **CSV Export**: Download query results as CSV
5. **Docker Setup**: Containerize the application

---

## 📝 Example Questions

Try these questions after setup:

- "Show all employees"
- "List products sorted by price"
- "Show orders from the last 30 days"
- "Count employees by department"
- "Show total revenue by product category"

---

## 🐛 Troubleshooting

### Database Connection Issues
```
# Verify MySQL is running
mysql -u root -p -e "SHOW DATABASES;"

# Check if sql_agent_db exists
mysql -u root -p -e "USE sql_agent_db; SHOW TABLES;"
```

### LLM Connection Issues
```
# Test Ollama connection
curl -X POST "https://aimodels.jadeglobal.com:8082/ollama/api/generate" \
  -d '{"model": "deepseek-coder:6.7b", "prompt": "Hello", "stream": false}'
```

### Migration Issues
```bash
cd backend
alembic upgrade head
alembic current
```

---

## 📜 License

MIT License
