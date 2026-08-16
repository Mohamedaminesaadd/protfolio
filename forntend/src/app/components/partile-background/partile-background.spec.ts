import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PartileBackground } from './partile-background';

describe('PartileBackground', () => {
  let component: PartileBackground;
  let fixture: ComponentFixture<PartileBackground>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PartileBackground]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PartileBackground);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
