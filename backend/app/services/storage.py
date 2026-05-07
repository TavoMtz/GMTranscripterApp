from ..database import supabase
import uuid

BUCKET_NAME = "audio-notes"


def upload_audio(file_path: str, original_filename: str) -> str:
    """
    Sube un archivo de audio al bucket 'audio-notas' de Supabase Storage.
    Retorna la URL pública del archivo subido.
    """
    # Generar nombre único para evitar colisiones entre archivos
    extension = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "wav"
    unique_name = f"{uuid.uuid4()}.{extension}"

    with open(file_path, "rb") as f:
        file_data = f.read()

    supabase.storage.from_(BUCKET_NAME).upload(
        path=unique_name,
        file=file_data,
        file_options={"content-type": f"audio/{extension}"}
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_name)
    return public_url
