import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { InmuebleDAO } from '../../services/inmuebles.dao';
import { GeneralDAO } from '../../services/general.dao';
import { Usuario } from '../../models/usuario.modelo';

@Component({
  selector: 'app-datos-tarjeta',
  standalone: true,
  imports: [FormsModule, MatDialogModule],
  templateUrl: './datos-tarjeta.component.html',
  styleUrl: './datos-tarjeta.component.css'
})
export class DatosTarjetaComponent {
  constructor(public dialogRef: MatDialogRef<DatosTarjetaComponent>, @Inject(MAT_DIALOG_DATA) public data: any, public inmuebleDAO: InmuebleDAO,
    private articuloService: GeneralDAO) { }

    public usuario: Usuario = {} as Usuario;

    ngOnInit(): void {
      this.loadUserData();
    }

    private async loadUserData(): Promise<void> {
      const usuario = await this.articuloService.getLocalUsuario();
      if (usuario !== null) {
        this.usuario = usuario;
      }
    }
  
    //Controlar mensajes (nota)
  async pagar(): Promise<void> {
    await this.inmuebleDAO.realizarAlquiler("InstantAbode/realizarAlquiler", this.data, this.usuario.id) || "";
    
    this.dialogRef.close();
  }

  async cancelar(): Promise<void> {
    this.dialogRef.close();
  }
}
