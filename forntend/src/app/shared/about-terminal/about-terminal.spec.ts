import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AboutTerminal } from './about-terminal';

describe('AboutTerminal', () => {
  let component: AboutTerminal;
  let fixture: ComponentFixture<AboutTerminal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AboutTerminal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AboutTerminal);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
