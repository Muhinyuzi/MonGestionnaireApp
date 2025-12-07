import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TachesComponent } from './taches.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';

describe('TachesComponent', () => {
  let component: TachesComponent;
  let fixture: ComponentFixture<TachesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TachesComponent],
      imports: [HttpClientTestingModule, FormsModule] // requis pour ngModel et HttpClient
    })
    .compileComponents();

    fixture = TestBed.createComponent(TachesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
