import { Component, Input, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-project-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './project-cart.html',
  styleUrl: './project-cart.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProjectCart {
  @Input({ required: true }) fileName!: string;
  @Input({ required: true }) fileIcon!: string;
  @Input() tags: string[] = [];
  @Input() liveUrl?: string;
  @Input() codeUrl?: string;
}