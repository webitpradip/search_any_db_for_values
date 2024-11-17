import os
from typing import Dict, Any, List, Tuple
import pymysql
import psycopg2
import pymongo
import pyodbc
from sqlalchemy import create_engine, text
from django.conf import settings

class DatabaseConnector:
    """Handles connections to different types of databases"""
    
    @staticmethod
    def get_connection(db_type: str, credentials: Dict[str, str]):
        """
        Create a connection based on database type
        """
        try:
            # Get password or empty string if not provided
            password = credentials.get('password', '')
            
            if db_type.lower() == 'mysql':
                return pymysql.connect(
                    host=credentials.get('host', 'localhost'),
                    user=credentials.get('username'),
                    password=password,
                    database=credentials.get('database')
                )
            
            elif db_type.lower() == 'postgresql':
                return psycopg2.connect(
                    host=credentials.get('host', 'localhost'),
                    user=credentials.get('username'),
                    password=password,
                    dbname=credentials.get('database')
                )
            
            elif db_type.lower() == 'mongodb':
                # Build MongoDB URI based on whether password is provided
                if password:
                    uri = f"mongodb://{credentials.get('username')}:{password}@{credentials.get('host', 'localhost')}/{credentials.get('database')}"
                else:
                    uri = f"mongodb://{credentials.get('host', 'localhost')}/{credentials.get('database')}"
                client = pymongo.MongoClient(uri)
                return client[credentials.get('database')]
            
            elif db_type.lower() == 'sqlserver':
                # Build SQL Server connection string based on whether password is provided
                if password:
                    conn_str = (
                        f"DRIVER={{SQL Server}};"
                        f"SERVER={credentials.get('host', 'localhost')};"
                        f"DATABASE={credentials.get('database')};"
                        f"UID={credentials.get('username')};"
                        f"PWD={password}"
                    )
                else:
                    conn_str = (
                        f"DRIVER={{SQL Server}};"
                        f"SERVER={credentials.get('host', 'localhost')};"
                        f"DATABASE={credentials.get('database')};"
                        f"UID={credentials.get('username')};"
                        f"Trusted_Connection=yes"
                    )
                return pyodbc.connect(conn_str)
            
            elif db_type.lower() == 'sqlite':
                engine = create_engine(f"sqlite:///{credentials.get('database')}")
                return engine.connect()
            
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
                
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {db_type}: {str(e)}")

class DatabaseSearcher:
    """Handles searching across different database types"""
    
    @staticmethod
    def search_all_tables(connection: Any, db_type: str, search_value: str) -> List[Dict[str, Any]]:
        """
        Search for a value across all tables in the database
        Returns a list of dictionaries containing table name, column name, and matching rows
        """
        results = []
        
        if db_type.lower() == 'mongodb':
            # MongoDB specific search
            for collection_name in connection.list_collection_names():
                collection = connection[collection_name]
                matches = collection.find({"$text": {"$search": search_value}})
                if matches:
                    results.append({
                        'table_name': collection_name,
                        'matches': list(matches)
                    })
        else:
            # SQL databases
            try:
                cursor = connection.cursor()
                
                # Get all tables
                if db_type.lower() == 'mysql':
                    cursor.execute("SHOW TABLES")
                elif db_type.lower() == 'postgresql':
                    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
                elif db_type.lower() == 'sqlserver':
                    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
                elif db_type.lower() == 'sqlite':
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                
                tables = [table[0] for table in cursor.fetchall()]
                
                # Search each table
                for table in tables:
                    
                    # Get columns for the table
                    if db_type.lower() in ['mysql', 'postgresql']:
                        cursor.execute(f"SELECT * FROM {table} LIMIT 0")
                        columns = [desc[0] for desc in cursor.description]
                    else:
                        # Generic approach for other databases
                        try:
                            cursor.execute(f"SELECT * FROM {table} WHERE 1=0")
                            columns = [desc[0] for desc in cursor.description]
                        except:
                            continue
                    
                    # Search each column
                    for column in columns:
                        if db_type.lower() == 'mysql':
                            query = f"SELECT * FROM {table} WHERE {column} LIKE \"%{search_value}%\""
                        elif db_type.lower() == 'postgresql':
                            query = f"SELECT * FROM {table} WHERE {column} ILIKE \"%{search_value}%\""
                        elif db_type.lower() == 'sqlite':
                            query = f"SELECT * FROM {table} WHERE {column} LIKE \"%{search_value}%\""
                        
                        
                        if db_type.lower() == 'sqlserver':
                            query = f"SELECT * FROM {table} WHERE CAST({column} AS NVARCHAR(MAX)) LIKE %{search_value}%"
                        
                        try:
                            cursor.execute(query)
                            matches = cursor.fetchall()
                            if matches:
                                results.append({
                                    'table_name': table,
                                    'column_name': column,
                                    'matches': matches,
                                    'columns': columns
                                })
                        except:
                            continue
                
                cursor.close()
                
            except Exception as e:
                raise Exception(f"Error searching database: {str(e)}")
        
        return results