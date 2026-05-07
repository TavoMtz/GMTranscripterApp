import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

export type ActiveView = 'transcription' | 'deepnotes';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './topbar.html',
  styleUrl: './topbar.css'
})
export class Topbar {
  @Input() title: string = '';
  @Input() tag: string = '';
  @Input() tagClass: string = 'tag-default';
  @Input() activeView: ActiveView = 'transcription';

  @Output() viewChanged = new EventEmitter<ActiveView>();

  setView(view: ActiveView) {
    if (this.activeView !== view) {
      this.viewChanged.emit(view);
    }
  }
}
