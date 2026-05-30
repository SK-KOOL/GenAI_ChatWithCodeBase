from app.services.voice_service import (
    speech_to_text,
    text_to_speech
)

from app.agents.codebase_agent import ask_codebase
from app.agents.sql_agent import ask_database


def process_voice_chat(
    audio_path: str,
    mode: str = "codebase"
):
    """
    Modes:
    - codebase
    - database
    """

    # Step 1: Speech To Text
    question = speech_to_text(audio_path)

    print("VOICE QUESTION:", question)

    # Step 2: Process Question

    if mode == "database":

        answer = ask_database(question)

    else:

        answer = ask_codebase(question)

    # Step 3: Text To Speech
    audio_response = text_to_speech(answer)

    return {
        "question": question,
        "answer": answer,
        "audio_path": audio_response
    }