from groq import Groq
from ..config import settings
import json

# Inicializar cliente de Groq
# Nota: Asegúrate de que GROQ_API_KEY esté en tu .env
client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """Eres un asistente experto en análisis de texto y lingüística. 
Tu tarea es analizar la transcripción de una nota de voz.

Instrucciones:
1. Genera un RESUMEN conciso que capture las ideas principales y cualquier tarea o fecha importante.
2. IMPORTANTE: El resumen DEBE estar en el MISMO IDIOMA que el texto original.
3. Genera una lista de ETIQUETAS (solo 1 por nota) para clasificar la nota (ej. "Trabajo", "Idea", "Recordatorio").

Debes responder ÚNICAMENTE en formato JSON válido:
{
  "summary": "texto del resumen",
  "tags": ["etiqueta1", "etiqueta2", "..."]
}"""

def analyze_transcription(raw_text: str) -> dict:
    """
    Usa Llama 3.3 70B vía Groq para resumir y etiquetar el texto.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Texto a analizar:\n\n{raw_text}"}
            ],
            temperature=0.1,
            response_format={"type": "json_object"} # Groq soporta modo JSON
        )
        
        result = json.loads(completion.choices[0].message.content)
        return {
            "summary": result.get("summary", ""),
            "tags": result.get("tags", [])
        }
    except Exception as e:
        print(f"Error en análisis LLM (Groq): {e}")
        return {"summary": "Error al generar resumen", "tags": []}
