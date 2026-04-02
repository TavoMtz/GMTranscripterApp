from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="GM Transcripter API")

@app.get("/")
async def root():
    return {"message": "API de Transcripción activa y funcionando 🚀"}

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    # Aquí es donde ocurrirá la magia de Whisper más adelante
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "Recibido correctamente"
    }