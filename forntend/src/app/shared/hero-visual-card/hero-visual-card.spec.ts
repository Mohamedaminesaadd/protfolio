import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HeroVisualCard } from './hero-visual-card';

describe('HeroVisualCard', () => {
  let component: HeroVisualCard;
  let fixture: ComponentFixture<HeroVisualCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeroVisualCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HeroVisualCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
