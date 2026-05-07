from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid
import os
import traceback
from .database import supabase
from .services.Ears import ears_service
from .services.storage import upload_audio as upload_audio_to_storage
from .services.transcriptions import save_transcription, get_all_transcriptions, update_transcription_analysis
from .services.brain import analyze_transcription
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


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Recibe un archivo de audio, lo transcribe con Whisper,
    sube el audio original a Supabase Storage y guarda el registro en la DB.
    """
    # Proteger contra filename nulo (blobs del MediaRecorder)
    original_filename = file.filename or f"recording-{uuid.uuid4()}.webm"

    # Nombre único para el archivo temporal (evita colisiones)
    extension = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "wav"
    temp_filename = f"{uuid.uuid4()}.{extension}"
    file_path = temp_dir / temp_filename

    # 1. Guardar archivo temporalmente
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"[1/6] Archivo temporal guardado: {file_path} ({os.path.getsize(file_path)} bytes)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo temporal: {str(e)}")

    try:
        # 2. Transcribir con Whisper
        print(f"[2/6] Transcribiendo con Whisper...")
        texto_transcrito = ears_service.transcribe_file(str(file_path))
        print(f"[2/6] Transcripción completada ({len(texto_transcrito)} chars)")

        # 3. Subir audio original al bucket 'audio-notes' en Supabase Storage
        print(f"[3/6] Subiendo a Supabase Storage...")
        audio_url = upload_audio_to_storage(str(file_path), original_filename)
        print(f"[3/6] Audio subido: {audio_url[:80]}...")

        # 4. Guardar registro en la tabla 'transcriptions'
        print(f"[4/6] Guardando registro en DB...")
        record = save_transcription(original_filename, texto_transcrito, audio_url)
        print(f"[4/6] Registro guardado con ID: {record.get('id')}")

        # 5. Análisis con Groq (Llama 3.3 70B)
        print(f"[5/6] Analizando con Groq...")
        analysis = analyze_transcription(texto_transcrito)
        print(f"[5/6] Análisis completado: {len(analysis.get('tags', []))} tags")

        # 6. Guardar análisis en DB
        transcription_id = record.get("id")
        if transcription_id:
            print(f"[6/6] Guardando análisis en DB...")
            update_transcription_analysis(
                transcription_id, 
                analysis["summary"], 
                analysis["tags"]
            )
            print(f"[6/6] Análisis guardado ✓")

        return {
            "id": record.get("id"),
            "filename": original_filename,
            "transcription": texto_transcrito,
            "audio_url": audio_url,
            "summary": analysis["summary"],
            "tags": analysis["tags"],
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en el proceso: {str(e)}")

    finally:
        # Siempre eliminar el archivo temporal
        if os.path.exists(file_path):
            os.unlink(file_path)


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