from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.codebase_routes import router as codebase_router
from app.api.sql_routes import router as sql_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(codebase_router)
app.include_router(sql_router)


@app.get("/")
def health():
    return {
        "message": "AI Platform Running"
    }