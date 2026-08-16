import { Component } from '@angular/core';

import { Editor } from '../../shared/editor/editor';
import { AboutTerminal } from '../../shared/about-terminal/about-terminal';
import { StatCard } from '../../shared/stat-card/stat-card';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [
    Editor,
    AboutTerminal,
    StatCard
  ],
  templateUrl: './about.html',
  styleUrl: './about.css',
})
export class About {

}