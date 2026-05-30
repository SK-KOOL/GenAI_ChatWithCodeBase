import os
import uuid
import traceback
import whisper

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from gtts import gTTS

from app.agents.codebase_agent import ask_codebase
from app.agents.sql_agent import ask_database
from app.agents.gemini_agent import ask_gemini

router = APIRouter()

# Whisper model
model = whisper.load_model("base")

# Base directory for this module (backend/app)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
AUDIOS_DIR = os.path.join(STATIC_DIR, "audio")
TEMP_DIR = os.path.join(BASE_DIR, "temp")


def ensure_directories():

    os.makedirs(STATIC_DIR, exist_ok=True)

    os.makedirs(AUDIOS_DIR, exist_ok=True)

    os.makedirs(TEMP_DIR, exist_ok=True)

@router.get("/voice-test")
def test():
    return {"message": "Voice route working"}

@router.post("/voice-chat")
async def voice_chat(
    file: UploadFile = File(...),
    mode: str = "codebase",
    repo_name: str = "default"
):

    try:

        ensure_directories()

        # Save uploaded audio
        audio_filename = f"{uuid.uuid4()}.wav"
        audio_path = os.path.join(TEMP_DIR, audio_filename)

        with open(audio_path, "wb") as buffer:

            buffer.write(await file.read())

        print("Audio Saved:", audio_path)

        # Speech To Text
        result = model.transcribe(
            audio_path,
            fp16=False
        )

        question = result["text"]

        print("Question:", question)

        # LLM Processing
        if mode == "db":

            answer = ask_database(question)

        elif mode == "codebase":

            answer = ask_codebase(repo_name, question)
        else:

            answer = ask_gemini(question)
            print("Answer:", answer)

        # Prevent None
        if not answer:
            answer = "No response generated"

        # Text To Speech
        tts = gTTS(
            text=str(answer),
            lang="en"
        )

        output_filename = f"{uuid.uuid4()}.mp3"
        output_path = os.path.join(AUDIOS_DIR, output_filename)
        tts.save(output_path)

        return {
            "success": True,
            "question": question,
            "answer": answer,
            "audio_url": f"/static/audio/{output_filename}"
        }

    except Exception as e:

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )