import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectCart } from './project-cart';

describe('ProjectCart', () => {
  let component: ProjectCart;
  let fixture: ComponentFixture<ProjectCart>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProjectCart]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProjectCart);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
