from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Any
import re

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.query_history import QueryHistory
from app.schemas.query_history import QueryRequest, QueryResponse

router = APIRouter(prefix="/query", tags=["Query"])


def validate_sql(query: str) -> bool:
    """Ensure only SELECT queries are allowed"""
    query_stripped = query.strip().upper()
    
    if not query_stripped.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")
    
    dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE", "CREATE", "GRANT", "REVOKE"]
    for keyword in dangerous_keywords:
        if keyword in query_stripped:
            raise ValueError(f"Dangerous operation '{keyword}' is prohibited.")
    
    return True


async def get_db_schema(db: Session) -> str:
    """Get database schema for LLM context"""
    # Get current database name
    result = db.execute(text("SELECT DATABASE()"))
    db_name = result.scalar()
    
    # Get all tables
    result = db.execute(text(f"""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_TYPE = 'BASE TABLE'
    """))
    tables = [row[0] for row in result.fetchall()]
    
    schema_parts = []
    for table in tables:
        result = db.execute(text(f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION
        """))
        columns = result.fetchall()
        col_strs = [f"  - {col[0]}: {col[1]} ({'NULL' if col[2]=='YES' else 'NOT NULL'})" + (" (PK)" if col[3]=='PRI' else "") for col in columns]
        schema_parts.append(f"Table: {table}\n" + "\n".join(col_strs))
    
    return "\n\n".join(schema_parts)


@router.get("/schema", response_model=dict)
async def get_schema(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get database schema for the user"""
    schema = await get_db_schema(db)
    return {"schema": schema}


@router.post("/execute", response_model=QueryResponse)
async def execute_query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Execute a natural language query:
    1. Validate the question
    2. Get schema context
    3. Save to history
    4. Execute and return results
    """
    from app.core.config import settings
    
    # For now, generate SQL from question (LLM integration would go here)
    # This is a placeholder that converts simple questions to SQL
    question_lower = request.question.lower()
    
    # Simple rule-based SQL generation (placeholder for LLM integration)
    sql, explanation = generate_sql_from_question(question_lower)
    
    # Validate SQL
    try:
        validate_sql(sql)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    # Execute query
    try:
        result = db.execute(text(sql))
        columns = result.keys()
        rows = result.fetchall()
        result_data = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SQL Execution Error: {str(e)}")
    
    # Save to history
    history_entry = QueryHistory(
        user_id=current_user.id,
        natural_question=request.question,
        generated_sql=sql,
        execution_result_json=result_data
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    
    return QueryResponse(
        sql=sql,
        explanation=explanation,
        result=result_data
    )


def generate_sql_from_question(question: str) -> tuple[str, str]:
    """
    Simple rule-based SQL generation (placeholder)
    In production, this would call OpenAI/Groq API
    """
    # This is a simplified placeholder
    # In production, integrate with OpenAI/Groq API
    
    if "employee" in question and "salary" in question:
        if "top" in question or "highest" in question:
            # Extract number if present
            import re
            num_match = re.search(r'\d+', question)
            num = num_match.group() if num_match else "5"
            return f"SELECT * FROM employees ORDER BY salary DESC LIMIT {num}", f"Retrieving top {num} employees by salary"
        elif "average" in question:
            return "SELECT AVG(salary) as avg_salary FROM employees", "Calculating average employee salary"
        else:
            return "SELECT * FROM employees", "Retrieving all employees with salary information"
    
    elif "department" in question:
        return "SELECT * FROM departments", "Retrieving all departments"
    
    elif "product" in question:
        if "price" in question and "above" in question:
            return "SELECT * FROM products ORDER BY price DESC", "Retrieving products sorted by price"
        else:
            return "SELECT * FROM products", "Retrieving all products"
    
    elif "order" in question:
        if "pending" in question:
            return "SELECT * FROM orders WHERE status = 'pending'", "Retrieving pending orders"
        else:
            return "SELECT * FROM orders", "Retrieving all orders"
    
    elif "count" in question and "employee" in question:
        return "SELECT COUNT(*) as total_employees FROM employees", "Counting total employees"
    
    else:
        # Default: return employees
        return "SELECT * FROM employees", "Showing employee data"
