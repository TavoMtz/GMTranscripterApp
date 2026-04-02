# GMTranscripterApp
App web que ayuda a las personas a tomar notas, documentar entrevistas o simplemente transcribir audios con un stack moderno de tecnologias.

# Estructura de carpetas
transcribe-ai-app/
├── backend/                # Lógica de FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints (v1, v2...)
│   │   ├── core/           # Configuración, seguridad, variables de entorno
│   │   ├── models/         # Modelos de Pydantic
│   │   ├── services/       # Lógica de Whisper, integración con LLMs
│   │   └── main.py         # Punto de entrada de FastAPI
│   ├── requirements.txt
│   └── .venv/              # Entorno virtual (excluido de git)
├── frontend/               # Proyecto de Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/ # Grabadora, lista de notas, visor de transcripción
│   │   │   ├── services/   # Comunicación con FastAPI y Supabase
│   │   │   └── guards/     # Protección de rutas (auth)
│   ├── angular.json
│   └── package.json
├── supabase/               # Todo lo relacionado con la DB y Auth
│   ├── migrations/         # Archivos .sql para replicar tu DB
│   └── config.toml         # Configuración local de Supabase
├── .mcp/                   # Configuraciones específicas para agentes de IA
│   └── custom-prompts.md   # Instrucciones para que el agente entienda tu DB
├── .gitignore              # ¡Crucial! Para no subir basura a GitHub
└── README.md               # Tu documentación técnica
