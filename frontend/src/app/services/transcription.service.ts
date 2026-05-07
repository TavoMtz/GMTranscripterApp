import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UploadResponse, TranscriptionResponse } from '../models/transcription.model';

@Injectable({
  providedIn: 'root',
})
export class TranscriptionService {
  private apiUrl = '/api';

  constructor(private httpClient: HttpClient) {}

  /** Sube un archivo de audio seleccionado por el usuario */
  uploadAudio(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.httpClient.post<UploadResponse>(`${this.apiUrl}/upload-audio`, formData);
  }

  /** Sube una grabación de audio capturada con MediaRecorder (Blob) */
  uploadRecording(blob: Blob, filename: string): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', blob, filename);
    return this.httpClient.post<UploadResponse>(`${this.apiUrl}/upload-audio`, formData);
  }

  /** Obtiene el historial de transcripciones */
  getTranscriptions(): Observable<TranscriptionResponse> {
    return this.httpClient.get<TranscriptionResponse>(`${this.apiUrl}/transcriptions`);
  }
}