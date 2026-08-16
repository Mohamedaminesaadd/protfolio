import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  inject
} from '@angular/core';

import {
  Router,
  RouterModule
} from '@angular/router';

@Component({
  selector: 'app-hero-visual-card',
  standalone: true,

  imports: [
    RouterModule
  ],

  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],

  templateUrl: './hero-visual-card.html',
  styleUrl: './hero-visual-card.css',
})
export class HeroVisualCard {

  private router = inject(Router);

  navigateTo(
    routeName: string,
    path: string
  ): void {

    console.log(
      `Navigating to ${routeName}: ${path}`
    );

    this.router.navigate([path]);
  }

}