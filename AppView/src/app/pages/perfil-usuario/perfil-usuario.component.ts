import { Component } from '@angular/core';
import { Usuario } from '../../models/usuario.modelo';
import { FormsModule } from '@angular/forms';
import { Location } from '@angular/common';
import { GeneralDAO } from '../../services/general.dao';

@Component({
  selector: 'app-perfil-usuario',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './perfil-usuario.component.html',
  styleUrl: './perfil-usuario.component.css'
})
export class PerfilUsuarioComponent {
  public usuario: Usuario = {} as Usuario;

  constructor(private location: Location, private articuloService: GeneralDAO) { }

  goBack(): void {
    this.location.back();
  }

  ngOnInit(): void {
    this.loadUserData();
  }

  cancelar() {
    this.location.back();  
  }

  private async loadUserData(): Promise<void> {
    const usuario = await this.articuloService.getLocalUsuario();
    if (usuario !== null) {
      this.usuario = usuario;
    }
  }
}
