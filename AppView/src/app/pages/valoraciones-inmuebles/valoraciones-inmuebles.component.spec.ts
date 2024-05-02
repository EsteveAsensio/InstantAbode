import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ValoracionesInmueblesComponent } from './valoraciones-inmuebles.component';

describe('ValoracionesInmueblesComponent', () => {
  let component: ValoracionesInmueblesComponent;
  let fixture: ComponentFixture<ValoracionesInmueblesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ValoracionesInmueblesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ValoracionesInmueblesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
