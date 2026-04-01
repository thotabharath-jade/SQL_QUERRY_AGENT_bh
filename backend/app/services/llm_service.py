import httpx
import json
from typing import Optional, List, Dict, Any
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.base_url = settings.LLAMA_BASE_URL
        self.model = settings.LLAMA_MODEL
        self.verify_ssl = settings.LLAMA_VERIFY_SSL
        
    async def generate_sql(
        self, 
        question: str, 
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate SQL query from natural language using LLM
        """
        # Build schema description
        schema_text = self._format_schema(schema)
        
        # Create the prompt
        prompt = f"""You are an expert SQL query generator. Based on the following database schema and user question, generate a valid SQL query.

DATABASE SCHEMA:
{schema_text}

USER QUESTION: {question}

IMPORTANT RULES:
1. Only generate SELECT queries (no INSERT, UPDATE, DELETE, DROP, or ALTER)
2. Use proper SQL syntax with appropriate JOINs if needed
3. Return ONLY the SQL query, nothing else
4. Do not include any explanations or markdown formatting
5. The query should be efficient and well-formatted

Generate the SQL query:"""

        try:
            response = await self._call_llm(prompt)
            return {
                "sql": response.strip(),
                "explanation": "Query generated successfully"
            }
        except Exception as e:
            return {
                "sql": "",
                "explanation": "",
                "error": str(e)
            }
    
    def _format_schema(self, schema: Dict[str, Any]) -> str:
        """Format schema dictionary into readable text"""
        lines = []
        for table in schema.get("tables", []):
            table_name = table.get("table_name")
            columns = table.get("columns", [])
            lines.append(f"\nTable: {table_name}")
            for col in columns:
                nullable = "NULL" if col.get("is_nullable") == "YES" else "NOT NULL"
                lines.append(f"  - {col.get('column_name')}: {col.get('data_type')} ({nullable})")
        return "\n".join(lines)
    
    async def _call_llm(self, prompt: str) -> str:
        """Make API call to Ollama"""
        async with httpx.AsyncClient(verify=self.verify_ssl, timeout=120.0) as client:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 2048
                }
            }
            
            response = await client.post(
                f"{self.base_url}/generate",
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"LLM API error: {response.status_code} - {response.text}")
            
            result = response.json()
            return result.get("response", "")


llm_service = LLMService()
