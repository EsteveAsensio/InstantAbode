import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatosCuentaBancariaComponent } from './datos-cuenta-bancaria.component';

describe('DatosCuentaBancariaComponent', () => {
  let component: DatosCuentaBancariaComponent;
  let fixture: ComponentFixture<DatosCuentaBancariaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DatosCuentaBancariaComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DatosCuentaBancariaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
