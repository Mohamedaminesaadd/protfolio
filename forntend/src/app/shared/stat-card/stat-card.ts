import { Component, input } from '@angular/core';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  templateUrl: './stat-card.html',
  styleUrl: './stat-card.css'
})
export class StatCard {

  value = input.required<string>();

  label = input.required<string>();

}