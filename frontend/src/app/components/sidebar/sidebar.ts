import { Component, Input, Output, EventEmitter, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Transcription } from '../../models/transcription.model';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css'
})
export class Sidebar implements OnChanges {
  @Input() transcriptions: Transcription[] = [];
  @Input() activeId: number | null = null;

  @Output() sessionSelected = new EventEmitter<Transcription>();

  ngOnChanges() {
    // If no active session and we have transcriptions, auto-select first
    if (this.activeId === null && this.transcriptions.length > 0) {
      this.sessionSelected.emit(this.transcriptions[0]);
    }
  }

  selectSession(t: Transcription) {
    this.sessionSelected.emit(t);
  }

  /** Derives display title from filename (strips extension) */
  getTitle(filename: string): string {
    return filename.replace(/\.[^/.]+$/, '');
  }

  /** Gets primary tag (first item) for display */
  getPrimaryTag(tags: string[] | null): string {
    return tags && tags.length > 0 ? tags[0] : '';
  }

  /** Maps a tag string to a CSS class for coloring */
  getTagClass(tag: string): string {
    if (!tag) return 'tag-default';
    const lower = tag.toLowerCase();
    if (['physics', 'math', 'chemistry', 'biology', 'science', 'ciencia', 'física'].some(k => lower.includes(k))) {
      return 'tag-science';
    }
    if (['spanish', 'english', 'french', 'german', 'idioma', 'language', 'español'].some(k => lower.includes(k))) {
      return 'tag-language';
    }
    if (['software', 'code', 'tech', 'programming', 'trabajo', 'development'].some(k => lower.includes(k))) {
      return 'tag-tech';
    }
    if (['research', 'academic', 'study', 'idea', 'investigación', 'estudio'].some(k => lower.includes(k))) {
      return 'tag-research';
    }
    return 'tag-default';
  }

  /** Returns a human-readable relative date */
  getRelativeDate(isoDate: string): string {
    const date = new Date(isoDate);
    const now = new Date();
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterdayStart = new Date(todayStart.getTime() - 86400000);
    const dateStart = new Date(date.getFullYear(), date.getMonth(), date.getDate());

    if (dateStart.getTime() === todayStart.getTime()) return 'Hoy';
    if (dateStart.getTime() === yesterdayStart.getTime()) return 'Ayer';

    // "May 5", "Jan 20", etc.
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
}
