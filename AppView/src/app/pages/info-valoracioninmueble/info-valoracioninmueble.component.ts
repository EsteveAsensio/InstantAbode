import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { ValoracionesDAO } from '../../services/valoraciones.dao';
import { SwalAnimation } from '../../utils/SwalAnimation';

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
      if(this.data.valoracion.comentario == "" || this.data.valoracion.comentario == null){
        await SwalAnimation.showCustomWarningMessageSwal("Advertencia " + "Comentario", "El comentario debe contener algo de contenido.");
      }else{
        const exito = await this.valoracionesDAO.modificarValoracionInmueble("InstantAbode/modificarValoracionInmueble", this.data.valoracion) || "";
        if (exito){
          SwalAnimation.showCustomSuccessSwal("Valoración modificada.");
        }
      }
    
    } else {
      // Crear nueva valoración
      const exito = await this.valoracionesDAO.addValoracionInmueble("InstantAbode/addValoracionInmueble", this.data.valoracion) || "";
      if (exito){
        SwalAnimation.showCustomSuccessSwal("Valoración añadida.");
      }
    }
    this.dialogRef.close();
  }
}
