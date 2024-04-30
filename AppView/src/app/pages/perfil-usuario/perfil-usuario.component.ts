import { Component } from '@angular/core';
import { Usuario } from '../../models/usuario.modelo';
import { FormsModule } from '@angular/forms';
import { Location } from '@angular/common';

@Component({
  selector: 'app-perfil-usuario',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './perfil-usuario.component.html',
  styleUrl: './perfil-usuario.component.css'
})
export class PerfilUsuarioComponent {
  public usuario: Usuario  = {} as Usuario;

  constructor(private location: Location) { }

  goBack(): void {
    this.location.back();
  }
}
