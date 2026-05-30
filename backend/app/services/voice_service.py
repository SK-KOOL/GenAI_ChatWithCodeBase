import whisper
import pyttsx3
import uuid
import os


# ==========================================
# CREATE REQUIRED DIRECTORIES AUTOMATICALLY
# ==========================================

BASE_DIR = "app"

STATIC_DIR = os.path.join(BASE_DIR, "static")

AUDIO_DIR = os.path.join(STATIC_DIR, "audio")

TEMP_DIR = os.path.join(BASE_DIR, "temp_audio")

os.makedirs(STATIC_DIR, exist_ok=True)

os.makedirs(AUDIO_DIR, exist_ok=True)

os.makedirs(TEMP_DIR, exist_ok=True)

# ==========================================
# LOAD WHISPER MODEL
# ==========================================

# Whisper Model
whisper_model = whisper.load_model("base")


def speech_to_text(audio_path: str):
    """
    Convert speech to text using Whisper
    """

    result = whisper_model.transcribe(audio_path)

    return result["text"]


def text_to_speech(text: str):
    """
    Convert text to speech
    """

    output_dir = "app/static/audio"

    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"

    filepath = os.path.join(output_dir, filename)

    engine = pyttsx3.init()

    engine.setProperty('rate', 170)

    engine.save_to_file(text, filepath)

    engine.runAndWait()

    return filepath.replace("\\", "/")