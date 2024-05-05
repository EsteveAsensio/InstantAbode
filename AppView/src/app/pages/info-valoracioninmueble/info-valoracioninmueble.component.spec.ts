import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoValoracioninmuebleComponent } from './info-valoracioninmueble.component';

describe('InfoValoracioninmuebleComponent', () => {
  let component: InfoValoracioninmuebleComponent;
  let fixture: ComponentFixture<InfoValoracioninmuebleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfoValoracioninmuebleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InfoValoracioninmuebleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
