# Plan de Implementación: Frontend (Angular)

Desarrollar una interfaz web moderna y premium para la gestión de transcripciones de audio, integrando las funcionalidades del backend FastAPI (transcripción con Whisper + análisis con Groq).

## User Review Required

> [!IMPORTANT]
> **CORS en el Backend**: Actualmente `main.py` **no** configura CORS. El frontend (Angular dev server en `http://localhost:4200`) no podrá comunicarse con el backend (`http://localhost:8000`) sin esta configuración. Se añadirá `CORSMiddleware` de FastAPI como primer paso.

> [!IMPORTANT]
> **Tecnología**: Se usará Angular 21 (CLI detectado: v21.2.0) con Standalone components y CSS puro. No se usará SSR.

## Open Questions

1. **¿Quieres algún color o branding específico?** El plan propone violetas/azules profundos con acentos neón sobre fondo oscuro. Si tienes preferencia de colores, dímelo.
2. **¿Necesitas autenticación (login) en esta primera versión?** El backend ya tiene un campo `user_id` en la tabla, pero no está implementado. Lo dejamos para después si no es prioridad.

---

## Proposed Changes

### Componente 0: CORS en el Backend (Requisito previo)

#### [MODIFY] [main.py](file:///c:/Users/alian/Desktop/Apps/GMTranscripterApp/backend/app/main.py)

Añadir middleware CORS para permitir peticiones desde el frontend Angular:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GM Transcripter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Componente 1: Inicialización del Proyecto Angular

Se inicializará un proyecto Angular en `frontend/` con esta configuración:

```bash
npx -y @angular/cli new gm-transcripter --directory ./ --style css --routing false --ssr false --skip-git --standalone --defaults --package-manager npm
```

**Justificación de flags:**
- `--directory ./`: Genera dentro de `frontend/` (se ejecutará desde ahí).
- `--routing false`: App de una sola vista, no necesita router por ahora.
- `--ssr false`: No necesitamos Server-Side Rendering.
- `--skip-git`: El repo Git ya existe en la raíz del monorepo.
- `--standalone`: Componentes standalone (sin NgModules).
- `--defaults`: Evita prompts interactivos.

---

### Componente 2: Proxy de Desarrollo

#### [NEW] `frontend/proxy.conf.json`

Redirige las peticiones `/api/*` al backend FastAPI durante el desarrollo:

```json
{
  "/api": {
    "target": "http://localhost:8000",
    "secure": false,
    "pathRewrite": {
      "^/api": ""
    }
  }
}
```

Se configurará en `angular.json` para que `ng serve` use este proxy automáticamente.

> [!NOTE]
> Con este proxy, el servicio Angular llamará a `/api/upload-audio` y el proxy lo reescribirá a `http://localhost:8000/upload-audio`. Así evitamos problemas de CORS en desarrollo (aunque CORS sigue siendo necesario para producción).

---

### Componente 3: Modelos e Interfaces TypeScript

#### [NEW] `frontend/src/app/models/transcription.model.ts`

Interfaces que mapean exactamente la respuesta del backend:

```typescript
// Respuesta de POST /upload-audio
export interface UploadResponse {
  id: string;
  filename: string;
  transcription: string;
  audio_url: string;
  summary: string;
  tags: string[];
}

// Cada item del array en GET /transcriptions
export interface Transcription {
  id: string;
  created_at: string;
  filename: string;
  audio_url: string;
  raw_text: string;
  summary: string | null;
  tags: string[] | null;
}

// Respuesta de GET /transcriptions
export interface TranscriptionListResponse {
  transcriptions: Transcription[];
  count: number;
}
```

> [!NOTE]
> Los campos `summary` y `tags` pueden ser `null` para registros antiguos que no pasaron por el análisis LLM.

---

### Componente 4: Servicio de API

#### [NEW] `frontend/src/app/services/transcription.service.ts`

```typescript
@Injectable({ providedIn: 'root' })
export class TranscriptionService {
  private apiUrl = '/api';

  uploadAudio(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);  // "file" coincide con el parámetro del backend
    return this.http.post<UploadResponse>(`${this.apiUrl}/upload-audio`, formData);
  }

  getTranscriptions(): Observable<TranscriptionListResponse> {
    return this.http.get<TranscriptionListResponse>(`${this.apiUrl}/transcriptions`);
  }
}
```

**Punto clave verificado**: El backend espera el campo `file` en el FormData (línea 34 de `main.py`: `file: UploadFile = File(...)`).

---

### Componente 5: Componentes de la Interfaz

#### [NEW] `frontend/src/app/components/header/`
Barra superior minimalista con el logo/nombre "GM Transcripter" y un indicador de estado.

#### [NEW] `frontend/src/app/components/audio-uploader/`
- Zona de drag-and-drop para archivos de audio.
- Botón "Seleccionar archivo" como alternativa.
- Estado visual de "Procesando..." con animación de pulso durante la subida + transcripción + análisis (el endpoint puede tardar varios segundos).
- Muestra un resumen de éxito con el `summary` generado.

#### [NEW] `frontend/src/app/components/transcription-card/`
Tarjeta individual que muestra:
- **Nombre del archivo** (`filename`).
- **Fecha** (`created_at`, formateada).
- **Resumen** (`summary`) — texto principal.
- **Etiquetas** (`tags`) — chips de colores.
- **Expandible**: Click para ver el texto completo (`raw_text`).
- **Audio**: Botón para reproducir el audio original (`audio_url`).

#### [NEW] `frontend/src/app/components/transcription-list/`
Contenedor que usa `TranscriptionService.getTranscriptions()` y renderiza una lista de `transcription-card`.

---

### Componente 6: Estética y Diseño Premium

- **Modo oscuro** como default: fondo `#0a0a1a` con gradientes sutiles.
- **Glassmorphism**: Tarjetas con `background: rgba(255,255,255,0.05)`, `backdrop-filter: blur(12px)`, bordes semi-transparentes.
- **Paleta de colores**:
  - Primario: `#7c3aed` (violeta).
  - Acento: `#06b6d4` (cyan).
  - Tags: Gradientes individuales por categoría.
- **Tipografía**: Google Fonts 'Inter' (body) + 'Outfit' (headings).
- **Micro-animaciones**:
  - Fade-in al cargar tarjetas.
  - Pulso en el uploader durante procesamiento.
  - Hover suave en tarjetas y botones.
- **Responsive**: Mobile-first con CSS Grid/Flexbox.

---

## Estructura de Archivos Final

```
frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── header/
│   │   │   ├── audio-uploader/
│   │   │   ├── transcription-card/
│   │   │   └── transcription-list/
│   │   ├── models/
│   │   │   └── transcription.model.ts
│   │   ├── services/
│   │   │   └── transcription.service.ts
│   │   ├── app.ts            # Componente raíz (Angular 21 style)
│   │   └── app.css
│   ├── index.html
│   └── styles.css            # Estilos globales (variables CSS, reset, fonts)
├── proxy.conf.json
├── angular.json
└── package.json
```

---

## Plan de Verificación

### Automated Tests
1. Arrancar backend: `cd backend && uvicorn app.main:app --reload`
2. Arrancar frontend: `cd frontend && ng serve --proxy-config proxy.conf.json`
3. Abrir `http://localhost:4200` en el navegador.

### Manual Verification
1. **Carga de Audio**: Subir un archivo `.wav` o `.mp3` → verificar que aparece el spinner de "Procesando..." → verificar que al terminar se muestra el resumen y tags.
2. **Historial**: Verificar que el historial carga con las transcripciones previas de Supabase.
3. **Reproducción**: Click en el botón de audio → verificar que reproduce el archivo desde Supabase Storage.
4. **Responsive**: Redimensionar la ventana → verificar que el layout se adapta correctamente.
