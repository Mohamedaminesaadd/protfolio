import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA
} from '@angular/core';

import { RouterOutlet } from '@angular/router';

import { MatrixBackground } from './components/matrix-back/matrix-back';
import { ParticleBackground } from './components/partile-background/partile-background';
import { Navbar } from './shared/navbar/navbar';

@Component({
  selector: 'app-root',
  standalone: true,

  imports: [
    RouterOutlet,
    MatrixBackground,
    ParticleBackground,
    Navbar
  ],

  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],

  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {}