import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MatrixBack } from './matrix-back';

describe('MatrixBack', () => {
  let component: MatrixBack;
  let fixture: ComponentFixture<MatrixBack>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatrixBack]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MatrixBack);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
