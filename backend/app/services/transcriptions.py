from ..database import supabase


def save_transcription(filename: str, raw_text: str, audio_url: str) -> dict:
    """
    Guarda un nuevo registro de transcripción en la tabla 'transcriptions'.
    user_id se deja en null (sin autenticación por ahora).
    Retorna la fila creada.
    """
    data = {
        "filename": filename,
        "audio_url": audio_url,
        "raw_text": raw_text,
    }
    response = supabase.table("transcriptions").insert(data).execute()
    return response.data[0] if response.data else data


def get_all_transcriptions() -> list:
    """
    Obtiene todas las transcripciones ordenadas de más reciente a más antigua.
    """
    response = (
        supabase.table("transcriptions")
        .select("id, created_at, filename, audio_url, raw_text, summary, tags")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data

def update_transcription_analysis(transcription_id: str, summary: str, tags: list) -> dict:
    """
    Actualiza el registro con el resumen y las etiquetas (TEXT[]).
    """
    data = {
        "summary": summary,
        "tags": tags
    }
    # Aseguramos que tags sea una lista para que el cliente de Supabase lo maneje como array de Postgres
    response = (
        supabase.table("transcriptions")
        .update(data)
        .eq("id", transcription_id)
        .execute()
    )
    return response.data[0] if response.data else data
