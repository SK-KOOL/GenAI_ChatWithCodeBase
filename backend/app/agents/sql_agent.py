import os

from sqlalchemy import text

from app.services.db_service import engine
from app.services.llm_service import llm

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import text


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


def generate_sql(question):

    prompt = f"""
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

    sql_query = generate_sql(question)
    
    print("sql_query 1:", sql_query)

    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")

    print("sql_query 2:", sql_query)
    result = execute_sql_query(sql_query)

    return {
        "sql": sql_query,
        "result": result
    }