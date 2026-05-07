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
- **Process Flow**: The backend relies on a temporary directory (`backend/temp/`) for saving audio uploads before transcription and uploading to Supabase Storage (`audio-notas` bucket).
- **LLM Integrations**: An implementation plan exists for auto-summaries and tagging (`implementation_plan_llm.md`). GPT-4o-mini is the recommended default. Ensure the `OPENAI_API_KEY` is present in the `.env` file for these features.

## Database & Storage (Supabase)
- **Tables**: The primary table is `transcriptions`. It expects a `summary` field and a `tags` field (array of text `text[]`).
- **Buckets**: Raw audio files are stored in the `audio-notas` bucket.

## Agent Guidelines
- **Path Context**: Always execute framework-specific commands from within their respective directories (e.g., `cd backend && ...`).
- **Language Convention**: The documentation, implementation plans, and inline code comments are predominantly in Spanish. When updating docs or adding descriptive comments, match this convention if requested or natural.
