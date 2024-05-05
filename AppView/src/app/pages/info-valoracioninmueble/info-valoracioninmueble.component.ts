import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { ValoracionesDAO } from '../../services/valoraciones.dao';

@Component({
  selector: 'app-info-valoracioninmueble',
  standalone: true,
  imports: [FormsModule, MatDialogModule],
  templateUrl: './info-valoracioninmueble.component.html',
  styleUrl: './info-valoracioninmueble.component.css'
})
export class InfoValoracioninmuebleComponent {
  constructor(
    public dialogRef: MatDialogRef<InfoValoracioninmuebleComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    public valoracionesDAO: ValoracionesDAO) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

  async save(): Promise<void> {
    if (this.data.valoracion.id) {
      // Actualizar una valoración existente
      await this.valoracionesDAO.modificarValoracionInmueble("InstantAbode/modificarValoracionInmueble", this.data.valoracion) || "";
    
    } else {
      // Crear nueva valoración
      await this.valoracionesDAO.addValoracionInmueble("InstantAbode/addValoracionInmueble", this.data.valoracion) || "";
    }
    this.dialogRef.close();
  }
}
