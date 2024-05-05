import { Component } from '@angular/core';
import { GeneralDAO } from '../../services/general.dao';
import { AuthService } from '../../services/auth-service';
import { FormsModule } from '@angular/forms';
import { CommonModule  } from '@angular/common';
import { Usuario } from '../../models/usuario.modelo';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { ValoracionInmueble } from '../../models/valoracionInmueble.modelo';
import { ValoracionesDAO } from '../../services/valoraciones.dao';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-valoraciones-inmuebles',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  templateUrl: './valoraciones-inmuebles.component.html',
  styleUrl: './valoraciones-inmuebles.component.css'
})
export class ValoracionesInmueblesComponent {
  constructor(private sanitizer: DomSanitizer, private articuloService: GeneralDAO, private valoracionesService: ValoracionesDAO, private authService: AuthService) { }

  valoraciones : ValoracionInmueble[] = [];
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
    this.valoraciones = await this.valoracionesService.obtenerValoracionesUsuario('InstantAbode/valoracionesUsuario/' + this.usuario.id) || [];
  }
  sanitizeImageUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }
}
