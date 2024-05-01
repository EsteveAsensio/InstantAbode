import { Component } from '@angular/core';
import { GeneralDAO } from '../../services/general.dao';
import { AuthService } from '../../services/auth-service';
import { Inmueble } from '../../models/inmueble.modelo';
import { FormsModule } from '@angular/forms';
import { CommonModule  } from '@angular/common';
import { InmuebleDAO } from '../../services/inmuebles.dao';
import { Usuario } from '../../models/usuario.modelo';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';

@Component({
  selector: 'app-inmuebles-alquilados',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  templateUrl: './inmuebles-alquilados.component.html',
  styleUrl: './inmuebles-alquilados.component.css'
})
export class InmueblesAlquiladosComponent {
  constructor(private articuloService: GeneralDAO, private inmueblesService: InmuebleDAO, private authService: AuthService) { }
  inmuebles: Inmueble[] = [];
  usuario: Usuario  = {} as Usuario;

  async ngOnInit(): Promise<void> {
    await this.loadUserData();
    this.cargarInmueblesUser();
  }

  private async loadUserData(): Promise<void> {
    const usuario = await this.articuloService.getLocalUsuario();
    if (usuario !== null) {
      this.usuario = usuario;
      console.log(this.usuario.id)
    }
  }

  async cargarInmueblesUser() {
    this.inmuebles = await this.inmueblesService.obtenerInmueblesAlquilados('InstantAbode/inmueblesAlquilados/' + this.usuario.id) || [];
  }

}
