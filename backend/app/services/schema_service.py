from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SchemaService:
    """Service for introspecting database schema"""
    
    @staticmethod
    async def get_database_schema(db: AsyncSession, database_name: str = "sql_agent_db") -> Dict[str, Any]:
        """
        Get complete database schema including tables, columns, and relationships
        """
        # Get all tables
        tables_query = text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :db_name 
            AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        result = await db.execute(tables_query, {"db_name": database_name})
        tables = [row[0] for row in result.fetchall()]
        
        schema = {"tables": []}
        
        for table_name in tables:
            table_schema = await SchemaService._get_table_schema(db, database_name, table_name)
            schema["tables"].append(table_schema)
        
        return schema
    
    @staticmethod
    async def _get_table_schema(
        db: AsyncSession, 
        database_name: str, 
        table_name: str
    ) -> Dict[str, Any]:
        """Get schema for a single table"""
        columns_query = text("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_KEY,
                EXTRA
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = :db_name 
            AND TABLE_NAME = :table_name
            ORDER BY ORDINAL_POSITION
        """)
        
        result = await db.execute(
            columns_query, 
            {"db_name": database_name, "table_name": table_name}
        )
        
        columns = []
        primary_key = None
        
        for row in result.fetchall():
            col_name, data_type, is_nullable, column_key, extra = row
            columns.append({
                "column_name": col_name,
                "data_type": data_type,
                "is_nullable": is_nullable,
                "is_primary_key": column_key == "PRI",
                "is_auto_increment": "auto_increment" in (extra or "").lower()
            })
            
            if column_key == "PRI":
                primary_key = col_name
        
        # Get foreign keys
        fk_query = text("""
            SELECT 
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = :db_name 
            AND TABLE_NAME = :table_name
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        
        result = await db.execute(
            fk_query, 
            {"db_name": database_name, "table_name": table_name}
        )
        
        foreign_keys = []
        for row in result.fetchall():
            foreign_keys.append({
                "column": row[0],
                "references_table": row[1],
                "references_column": row[2]
            })
        
        return {
            "table_name": table_name,
            "columns": columns,
            "primary_key": primary_key,
            "foreign_keys": foreign_keys
        }


schema_service = SchemaService()
