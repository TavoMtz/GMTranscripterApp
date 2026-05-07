import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Transcription } from './models/transcription.model';
import { TranscriptionService } from './services/transcription.service';
import { Sidebar } from './components/sidebar/sidebar';
import { Topbar, ActiveView } from './components/topbar/topbar';
import { ContentView } from './components/content-view/content-view';
import { RecordingBar } from './components/recording-bar/recording-bar';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, Sidebar, Topbar, ContentView, RecordingBar],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  transcriptions = signal<Transcription[]>([]);
  activeTranscription = signal<Transcription | null>(null);
  activeView = signal<ActiveView>('transcription');
  isLoading = signal(true);

  constructor(private transcriptionService: TranscriptionService) {}

  ngOnInit() {
    this.loadTranscriptions();
  }

  loadTranscriptions() {
    this.isLoading.set(true);
    this.transcriptionService.getTranscriptions().subscribe({
      next: (res) => {
        const list = res.transcriptions || [];
        this.transcriptions.set(list);
        // Auto-select first if nothing is active
        if (!this.activeTranscription() && list.length > 0) {
          this.activeTranscription.set(list[0]);
        }
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }

  onSessionSelected(t: Transcription) {
    this.activeTranscription.set(t);
  }

  onViewChanged(view: ActiveView) {
    this.activeView.set(view);
  }

  onRecordingComplete() {
    this.loadTranscriptions();
  }

  getActiveTitle(): string {
    const t = this.activeTranscription();
    if (!t) return '';
    return t.filename.replace(/\.[^/.]+$/, '');
  }

  getActiveTag(): string {
    const t = this.activeTranscription();
    if (!t || !t.tags || t.tags.length === 0) return '';
    return t.tags[0];
  }

  getActiveTagClass(): string {
    const tag = this.getActiveTag().toLowerCase();
    if (!tag) return 'tag-default';
    if (['physics','math','chemistry','biology','science','ciencia','física'].some(k => tag.includes(k))) return 'tag-science';
    if (['spanish','english','french','german','idioma','language','español'].some(k => tag.includes(k))) return 'tag-language';
    if (['software','code','tech','programming','trabajo','development'].some(k => tag.includes(k))) return 'tag-tech';
    if (['research','academic','study','idea','investigación','estudio'].some(k => tag.includes(k))) return 'tag-research';
    return 'tag-default';
  }
}
