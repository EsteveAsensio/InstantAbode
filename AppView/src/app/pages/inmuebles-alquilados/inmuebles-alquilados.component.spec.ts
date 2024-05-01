import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InmueblesAlquiladosComponent } from './inmuebles-alquilados.component';

describe('InmueblesAlquiladosComponent', () => {
  let component: InmueblesAlquiladosComponent;
  let fixture: ComponentFixture<InmueblesAlquiladosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InmueblesAlquiladosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InmueblesAlquiladosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
