import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA
} from '@angular/core';

@Component({
  selector: 'app-about-terminal',
  standalone: true,

  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],

  templateUrl: './about-terminal.html',
  styleUrl: './about-terminal.css'
})
export class AboutTerminal {}