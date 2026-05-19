"""
Orquestador: Conecta Ears (escucha) con Brain (análisis).
"""
from .Ears import ears_service
from .brain import analyze_transcription


def process_audio(file_path: str) -> dict:
    """
    Pipeline de inteligencia:
    1. Ears escucha el audio → texto
    2. Brain analiza el texto → resumen + tags
    """
    # Escuchar
    raw_text = ears_service.transcribe_file(file_path)

    # Pensar
    analysis = analyze_transcription(raw_text)

    return {
        "transcription": raw_text,
        "summary": analysis["summary"],
        "tags": analysis["tags"],
    }
