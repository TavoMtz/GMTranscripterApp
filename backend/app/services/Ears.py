import whisper
import os

class Ears():
    def __init__(self):
        print("Cargando modelo")
        self.model = whisper.load_model("base")

    def transcribe_file(self, path):
        if not os.path.exists(path):
            return "Error: El archivo no existe."
            
        try:
            # fp16=False es importante si no tienes una GPU potente (evita warnings y mejora CPU)
            result = self.model.transcribe(path, fp16=False)
            return result["text"].strip()
        except Exception as e:
            return f"Error durante la transcripción: {str(e)}"

# Se crea la instancia global para que el modelo se cargue al importar el servicio
ears_service = Ears()
