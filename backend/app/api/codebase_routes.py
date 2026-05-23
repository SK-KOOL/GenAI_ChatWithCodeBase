import os

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.repo_service import clone_repository

from app.agents.codebase_agent import (
    ingest_repository,
    ask_codebase
)

router = APIRouter()


class RepoRequest(BaseModel):
    repo_url: str


class ChatRequest(BaseModel):
    repo_name: str
    question: str


@router.post("/clone-repository")
def clone_repo(data: RepoRequest):

    repo_path = clone_repository(data.repo_url)

    repo_name = repo_path.split("/")[-1]

    ingest_repository(repo_path, repo_name)

    return {
        "message": "Repository cloned successfully",
        "repo_name": repo_name
    }


@router.post("/chat-codebase")
def chat_codebase(data: ChatRequest):

    answer = ask_codebase(
        data.repo_name,
        data.question
    )

    return {
        "answer": answer
    }