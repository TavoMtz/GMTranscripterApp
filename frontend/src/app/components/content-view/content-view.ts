import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Transcription } from '../../models/transcription.model';
import { ActiveView } from '../topbar/topbar';

@Component({
  selector: 'app-content-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './content-view.html',
  styleUrl: './content-view.css'
})
export class ContentView {
  @Input() transcription: Transcription | null = null;
  @Input() activeView: ActiveView = 'transcription';

  /** Splits raw_text into paragraphs for readability */
  getParagraphs(text: string | null): string[] {
    if (!text) return [];
    // Split on double newlines or long sentences ending in period followed by space
    const parts = text.split(/\n\n+/).filter(p => p.trim().length > 0);
    return parts.length > 1 ? parts : [text];
  }

  /**
   * Extracts key points from tags.
   * The tags represent categories; we use summary bullet heuristics if possible.
   * For now, display tags as key point labels since the backend doesn't return separate bullet points.
   */
  getKeyPoints(tags: string[] | null): string[] {
    if (!tags || tags.length === 0) return [];
    return tags;
  }
}
