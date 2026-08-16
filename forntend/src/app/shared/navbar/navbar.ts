import { isPlatformBrowser } from '@angular/common';
import { Component, CUSTOM_ELEMENTS_SCHEMA, inject, PLATFORM_ID } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class Navbar {
  private readonly isBrowser = isPlatformBrowser(inject(PLATFORM_ID));

  constructor(readonly router: Router) {}

  navigateTo(sectionId: string, path: string): void {
    if (sectionId === 'chat') {
      void this.router.navigateByUrl(path);
      return;
    }

    void this.router.navigateByUrl(path).then(() => {
      if (!this.isBrowser) return;

      requestAnimationFrame(() => {
        document.getElementById(sectionId)?.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      });
    });
  }

}
