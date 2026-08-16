import { Component } from '@angular/core';

import { Terminal } from '../../shared/terminal/terminal';
import { HeroVisualCard } from '../../shared/hero-visual-card/hero-visual-card';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    Terminal,
    HeroVisualCard,
  ],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {}