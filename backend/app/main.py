from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Base directory for this module (backend/app)
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
AUDIOS_DIR = os.path.join(STATIC_DIR, "audio")
TEMP_AUDIO_DIR = os.path.join(BASE_DIR, "temp_audio")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(AUDIOS_DIR, exist_ok=True)
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

# Import routes
from app.api.codebase_routes import router as codebase_router
from app.api.sql_routes import router as sql_router
from app.api.voice_routes import router as voice_router

# FastAPI app
app = FastAPI(title="AI Codebase Assistant", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (serve backend/app/static)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Routes
app.include_router(codebase_router, prefix="/api", tags=["Codebase"]) 
app.include_router(sql_router, prefix="/api", tags=["Database"]) 
app.include_router(voice_router, prefix="/api", tags=["Voice Assistant"]) 


@app.get("/")
def root():
    return {"message": "Backend Running Successfully"}