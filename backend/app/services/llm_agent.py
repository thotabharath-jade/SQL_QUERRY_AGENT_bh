"""
LLM Agent Service
This module handles the integration with OpenAI/Groq API for SQL generation.
"""
from typing import Optional
from app.core.config import settings


class LLMAgent:
    """
    LLM Agent that converts natural language questions to SQL queries.
    
    In production, this would integrate with OpenAI/Groq API.
    For now, it uses a simple rule-based approach.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.LLM_MODEL
    
    def generate_sql(self, question: str, schema: str) -> dict:
        """
        Convert a natural language question to SQL.
        
        Args:
            question: The natural language question
            schema: The database schema description
            
        Returns:
            dict with 'sql' and 'explanation' keys
        """
        # Placeholder implementation - in production, call OpenAI/Groq API
        # 
        # Example OpenAI call:
        # response = openai.ChatCompletion.create(
        #     model=self.model,
        #     messages=[
        #         {"role": "system", "content": f"You are a SQL expert. Schema:\n{schema}"},
        #         {"role": "user", "content": question}
        #     ]
        # )
        # return {"sql": response.choices[0].message.content, "explanation": "..."}
        
        # For now, return a placeholder response
        return {
            "sql": "-- LLM integration pending. Configure OPENAI_API_KEY in .env",
            "explanation": "Configure your OpenAI API key to enable LLM-based SQL generation."
        }
    
    def validate_and_fix_sql(self, sql: str, schema: str) -> dict:
        """
        Validate and potentially fix SQL queries.
        
        Args:
            sql: The SQL query to validate
            schema: The database schema description
            
        Returns:
            dict with 'sql', 'is_valid', and 'error' keys
        """
        # Placeholder validation
        sql_upper = sql.strip().upper()
        
        if not sql_upper.startswith("SELECT"):
            return {
                "sql": sql,
                "is_valid": False,
                "error": "Only SELECT queries are allowed"
            }
        
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE", "CREATE"]
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return {
                    "sql": sql,
                    "is_valid": False,
                    "error": f"Dangerous operation '{keyword}' is prohibited"
                }
        
        return {
            "sql": sql,
            "is_valid": True,
            "error": None
        }


# Singleton instance
llm_agent = LLMAgent()
