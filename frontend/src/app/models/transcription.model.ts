export interface UploadResponse {
    id: number;
    filename: string;
    transcription: string;
    audio_url: string;
    summary: string;
    tags: string[];
}

export interface Transcription {
    id: number;
    filename: string;
    audio_url: string;
    raw_text: string;
    summary: string | null;
    tags: string[] | null;
    created_at: string;
}

export interface TranscriptionResponse {
    transcriptions: Transcription[];
    count: number;
}