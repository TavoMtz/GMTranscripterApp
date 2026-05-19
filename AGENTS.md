# OpenCode Agent Instructions

This repository is a monorepo containing a modern web app for audio transcription using AI (Whisper + LLMs).

## Project Structure & Architecture
- `backend/`: FastAPI application in Python. Entrypoint is `backend/app/main.py`.
- `frontend/`: Angular application.
- `supabase/`: Database, authentication, and storage configuration.

## Backend Development (FastAPI)
- **Tech Stack**: Uses `uvicorn` as the server, `supabase` client for DB/Storage, and `openai-whisper` for local transcription.
- **Setup**: Ensure the Python virtual environment (`backend/.venv/`) is active and dependencies from `backend/requirements.txt` are installed.
- **Running locally**: Run `uvicorn app.main:app --reload` from the `backend/` directory to start the dev server.
- **Process Flow**: The backend uses a non-blocking asynchronous architecture. Audio uploads are temporarily saved to `backend/temp/`, processed by an orchestrator service (Ears for transcription, Brain for analysis), and immediately returns a response to the user. Supabase storage upload and database persistence are handled via FastAPI BackgroundTasks.
- **LLM Integrations**: Auto-summaries and tagging are implemented using Groq's Llama 3.3 70B model via the Brain service (`services/brain.py`). Ensure the `GROQ_API_KEY` is present in the `.env` file.

## Database & Storage (Supabase)
- **Tables**: The primary table is `transcriptions`. It expects a `summary` field and a `tags` field (array of text `text[]`).
- **Buckets**: Raw audio files are stored in the `audio-notas` bucket.

## Agent Guidelines
- **Path Context**: Always execute framework-specific commands from within their respective directories (e.g., `cd backend && ...`).
- **Language Convention**: The documentation, implementation plans, and inline code comments are predominantly in Spanish. When updating docs or adding descriptive comments, match this convention if requested or natural.
