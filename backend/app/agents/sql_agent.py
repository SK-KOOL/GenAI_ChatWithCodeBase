import os

from sqlalchemy import create_engine,text

from app.services.db_service import engine
from app.services.llm_service import llm

from dotenv import load_dotenv

from sqlalchemy.exc import SQLAlchemyError
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PASSWORD = DB_PASSWORD.replace("@", "%40") # Encode @ symbol for URL
DB_PASSWORD = DB_PASSWORD.replace(":", "%3A") # Encode : symbol for URL
DB_PASSWORD = DB_PASSWORD.replace("/", "%2F") # Encode / symbol for URL
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

def get_database_schema():

    schema = ""

    with engine.connect() as conn:

        tables = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
        """))

        for table in tables:

            table_name = table[0]

            schema += f"\nTable: {table_name}\n"

            columns = conn.execute(text(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = DATABASE()
                AND table_name = '{table_name}'
            """))

            for column in columns:
                schema += f"- {column[0]} ({column[1]})\n"

    return schema


def generate_sql(question, schema):

    prompt = f"""

    You are an expert MySQL SQL generator.

    IMPORTANT RULES:
    1. ONLY use tables/columns from schema
    2. NEVER hallucinate columns
    3. Return ONLY SQL query
    4. Use MySQL syntax
    5. Do not use markdown

    DATABASE SCHEMA:
    {schema}

    USER QUESTION:
    {question}

    Convert user question into SQL query.

    Only return SQL query.

    Database is MySQL.

    Question:
    {question}

    Return ONLY SQL query.
    """

    response = llm.invoke(prompt)

    return response.content.strip()


def execute_sql_query(query):
    FORBIDDEN = [
        "delete",
        "update",
        "drop",
        "truncate",
        "insert",
        "alter"
    ]

    lower_query = query.lower()

    if any(word in lower_query for word in FORBIDDEN):
        raise Exception("Only SELECT queries allowed")
    
    with engine.connect() as conn:

        result = conn.execute(text(query))

        rows = [dict(row._mapping) for row in result]

        return rows


def ask_database(question):
    try:

        schema = get_database_schema()

        print("\n=========== DATABASE SCHEMA ===========")
        print(schema)
        sql_query = generate_sql(question, schema)
        
        print("sql_query 1:", sql_query)

        sql_query = sql_query.replace("```sql", "")
        sql_query = sql_query.replace("```", "")

        print("sql_query 2:", sql_query)
        result = execute_sql_query(sql_query)

        return {
            "success": True,
            "sql": sql_query,
            "result": result
        }
    except SQLAlchemyError as e:

        return {
            "success": False,
            "error": str(e)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }