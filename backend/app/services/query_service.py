import re
from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings


class QueryService:
    """Service for executing SQL queries safely"""
    
    DANGEROUS_KEYWORDS = [
        "DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE", 
        "CREATE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "SHOW", "DESCRIBE"
    ]
    
    @staticmethod
    def validate_sql(query: str) -> tuple[bool, str]:
        """
        Validate SQL query for safety.
        Returns (is_valid, error_message)
        """
        query_stripped = query.strip().upper()
        
        # Check if it starts with SELECT
        if not query_stripped.startswith("SELECT"):
            return False, "Only SELECT queries are allowed."
        
        # Check for dangerous keywords
        for keyword in QueryService.DANGEROUS_KEYWORDS:
            # Use word boundary matching to avoid false positives
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, query_stripped):
                return False, f"Query contains forbidden keyword: {keyword}"
        
        # Check for multiple statements (semicolon followed by more SQL)
        if ';' in query_stripped[6:]:  # Check after SELECT
            return False, "Multiple statements are not allowed."
        
        return True, ""
    
    @staticmethod
    async def execute_query(
        db: AsyncSession, 
        query: str,
        max_rows: int = None
    ) -> Dict[str, Any]:
        """
        Execute a SELECT query and return results.
        Returns dict with columns, rows, and row_count
        """
        if max_rows is None:
            max_rows = settings.MAX_QUERY_ROWS
        
        # Add LIMIT if not present
        query = query.strip()
        if query.upper()[-6:] != "LIMIT 1" and " LIMIT " not in query.upper():
            query = f"{query} LIMIT {max_rows}"
        
        try:
            result = await db.execute(text(query))
            rows = result.fetchall()
            columns = list(result.keys())
            
            # Convert rows to list of dicts
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
            
            return {
                "success": True,
                "columns": columns,
                "rows": data,
                "row_count": len(data)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "columns": [],
                "rows": [],
                "row_count": 0
            }


query_service = QueryService()
