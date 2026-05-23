from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.sql_agent import ask_database

router = APIRouter()


class SQLRequest(BaseModel):
    question: str


@router.post("/ask-database")
def ask_db(data: SQLRequest):

    response = ask_database(data.question)

    return response