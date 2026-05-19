from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pathlib import Path
import shutil
import uuid
import os
import traceback
from .database import supabase
from .services.orchestrator import process_audio
from .services.storage import upload_audio as upload_audio_to_storage
from .services.transcriptions import save_transcription, get_all_transcriptions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GM Transcripter API")
origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Directorio temporal para guardar audios antes de transcribir
temp_dir = Path("temp")
temp_dir.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "API de Transcripción activa y funcionando 🚀"}


@app.get("/check-db")
async def check_db():
    try:
        supabase.table("transcriptions").select("*").limit(0).execute()
        return {"status": "Conexión Exitosa", "table": "transcriptions"}
    except Exception as e:
        return {"status": "Error de Conexión", "detail": str(e)}



def _persist_in_background(file_path: str, original_filename: str, result: dict):
    """Tarea de background: guardar en Storage y DB, luego limpiar el temporal."""
    try:
        # Subir audio a Supabase Storage
        print(f"[BG] Subiendo audio a Storage...")
        audio_url = upload_audio_to_storage(file_path, original_filename)
        print(f"[BG] Audio subido: {audio_url[:80]}...")

        # Guardar registro completo en DB (un solo INSERT)
        print(f"[BG] Guardando registro en DB...")
        save_transcription(
            filename=original_filename,
            raw_text=result["transcription"],
            audio_url=audio_url,
            summary=result["summary"],
            tags=result["tags"],
        )
        print(f"[BG] Registro guardado ✓")
    except Exception as e:
        print(f"[BG] Error al persistir: {e}")
    finally:
        # Limpiar archivo temporal
        if os.path.exists(file_path):
            os.unlink(file_path)
            print(f"[BG] Archivo temporal eliminado ✓")


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Recibe audio, lo procesa (Ears → Brain), responde rápido y persiste en background."""
    # Proteger contra filename nulo (blobs del MediaRecorder)
    original_filename = file.filename or f"recording-{uuid.uuid4()}.webm"

    # Nombre único para el archivo temporal (evita colisiones)
    extension = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "wav"
    file_path = temp_dir / f"{uuid.uuid4()}.{extension}"

    # Guardar archivo temporalmente (responsabilidad HTTP)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"[📥] Archivo temporal guardado: {file_path} ({os.path.getsize(file_path)} bytes)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo temporal: {str(e)}")

    try:
        # 🎯 Pipeline de inteligencia (Ears → Brain)
        result = process_audio(str(file_path))

        # Persistir en background (no bloquea al usuario)
        background_tasks.add_task(
            _persist_in_background, str(file_path), original_filename, result
        )

        # Responder inmediatamente
        return {
            "filename": original_filename,
            "transcription": result["transcription"],
            "summary": result["summary"],
            "tags": result["tags"],
        }

    except Exception as e:
        # Si falla el pipeline, limpiar el archivo
        if os.path.exists(file_path):
            os.unlink(file_path)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en el proceso: {str(e)}")



@app.get("/transcriptions")
async def list_transcriptions():
    """
    Devuelve el historial completo de transcripciones,
    ordenadas de más reciente a más antigua.
    """
    try:
        data = get_all_transcriptions()
        return {"transcriptions": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar historial: {str(e)}")