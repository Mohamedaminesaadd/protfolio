import {
  Component,
  Input,
  CUSTOM_ELEMENTS_SCHEMA
} from '@angular/core';

import { CommonModule } from '@angular/common';

export interface Skill {
  name: string;
  icon: string;
}

@Component({
  selector: 'app-skills-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './skills-card.html',
  styleUrl: './skills-card.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class SkillsCard {

  @Input({ required: true })
  categoryName!: string;

  @Input({ required: true })
  categoryIcon!: string;

  @Input({ required: true })
  skills: Skill[] = [];
}