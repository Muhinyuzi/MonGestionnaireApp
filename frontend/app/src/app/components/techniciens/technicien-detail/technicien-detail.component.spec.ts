import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TechnicienDetailComponent } from './technicien-detail.component';

describe('TechnicienDetailComponent', () => {
  let component: TechnicienDetailComponent;
  let fixture: ComponentFixture<TechnicienDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TechnicienDetailComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TechnicienDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
