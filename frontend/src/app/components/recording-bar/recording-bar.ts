import {
  Component,
  Output,
  EventEmitter,
  OnDestroy,
  signal,
  ElementRef,
  ViewChild
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranscriptionService } from '../../services/transcription.service';
import { UploadResponse } from '../../models/transcription.model';

export type RecordingState = 'idle' | 'recording' | 'saved';

@Component({
  selector: 'app-recording-bar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recording-bar.html',
  styleUrl: './recording-bar.css'
})
export class RecordingBar implements OnDestroy {
  @Output() recordingComplete = new EventEmitter<UploadResponse>();
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  state = signal<RecordingState>('idle');
  timerDisplay = signal('0:00');
  errorMsg = signal<string | null>(null);

  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  private timerInterval: ReturnType<typeof setInterval> | null = null;
  private elapsedSeconds = 0;

  constructor(private transcriptionService: TranscriptionService) {}

  // ─── Public toggle (called by template) ───────────────────────────────────
  toggleRecording() {
    if (this.state() === 'recording') {
      this.stopRecording();
    } else if (this.state() === 'idle') {
      this.startRecording();
    }
  }

  // ─── Recording ────────────────────────────────────────────────────────────
  private async startRecording() {
    this.errorMsg.set(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.audioChunks = [];
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) this.audioChunks.push(e.data);
      };

      this.mediaRecorder.onstop = () => {
        // Stop all mic tracks
        stream.getTracks().forEach(t => t.stop());
        this.onRecordingStopped();
      };

      this.mediaRecorder.start(250); // collect chunks every 250ms
      this.state.set('recording');
      this.startTimer();

    } catch (err) {
      console.error('Microphone access denied:', err);
      this.errorMsg.set('No se pudo acceder al micrófono. Verifica los permisos.');
    }
  }

  private stopRecording() {
    this.stopTimer();
    this.mediaRecorder?.stop();
    // State transitions happen in onstop callback
  }

  private onRecordingStopped() {
    this.state.set('saved');

    const blob = new Blob(this.audioChunks, { type: 'audio/webm' });
    const filename = `nota-${this.formatDateForFilename()}.webm`;

    this.transcriptionService.uploadRecording(blob, filename).subscribe({
      next: (response) => {
        this.recordingComplete.emit(response);
        this.resetToIdle();
      },
      error: (err) => {
        console.error('Upload error:', err);
        this.errorMsg.set('Error al subir la grabación. Intenta de nuevo.');
        this.resetToIdle();
      }
    });

    // Also reset after 2.5s regardless of upload state (as per spec)
    setTimeout(() => {
      if (this.state() === 'saved') {
        this.resetToIdle();
      }
    }, 2500);
  }

  // ─── File upload (drag & import) ──────────────────────────────────────────
  openFileDialog() {
    this.fileInput?.nativeElement.click();
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.uploadFile(input.files[0]);
      input.value = ''; // reset so same file can be reselected
    }
  }

  private uploadFile(file: File) {
    if (!file.type.startsWith('audio/')) {
      this.errorMsg.set('Selecciona un archivo de audio válido.');
      return;
    }
    this.errorMsg.set(null);
    this.state.set('saved');

    this.transcriptionService.uploadAudio(file).subscribe({
      next: (response) => {
        this.recordingComplete.emit(response);
        this.resetToIdle();
      },
      error: (err) => {
        console.error('Upload error:', err);
        this.errorMsg.set('Error al subir el archivo. Intenta de nuevo.');
        this.resetToIdle();
      }
    });
  }

  // ─── Timer ────────────────────────────────────────────────────────────────
  private startTimer() {
    this.elapsedSeconds = 0;
    this.timerDisplay.set('0:00');
    this.timerInterval = setInterval(() => {
      this.elapsedSeconds++;
      const m = Math.floor(this.elapsedSeconds / 60);
      const s = this.elapsedSeconds % 60;
      this.timerDisplay.set(`${m}:${s.toString().padStart(2, '0')}`);
    }, 1000);
  }

  private stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  private resetToIdle() {
    this.state.set('idle');
    this.stopTimer();
    this.elapsedSeconds = 0;
    this.timerDisplay.set('0:00');
  }

  private formatDateForFilename(): string {
    const now = new Date();
    return now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
  }

  // ─── Lifecycle ────────────────────────────────────────────────────────────
  ngOnDestroy() {
    this.stopTimer();
    if (this.mediaRecorder?.state === 'recording') {
      this.mediaRecorder.stop();
    }
  }
}
