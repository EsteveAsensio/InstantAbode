import { Component } from '@angular/core';
import { GeneralDAO } from '../../services/general.dao';
import { AuthService } from '../../services/auth-service';
import { Inmueble } from '../../models/inmueble.modelo';
import { FormsModule } from '@angular/forms';
import { CommonModule, formatDate  } from '@angular/common';

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './principal.component.html',
  styleUrl: './principal.component.css'
})
export class PrincipalComponent {


  constructor(private articuloService: GeneralDAO, private authService: AuthService) { }

  fechaInicio: Date | undefined = undefined;
  fechaFinal: Date | undefined = undefined;

  provinciaSelec: string = ''

  provincias: String[] = [];
  inmuebles: Inmueble[] = [];

  ngOnInit(): void {
    this.cargarProvincias();
  }

  async cargarProvincias() {
    this.provincias = await this.articuloService.getGeneral('InstantAbode/provincias') || [];
  }

  async loadInmuebles() {
    if (this.fechaFinal !== undefined && this.fechaInicio !== undefined && this.provinciaSelec !== ''){
      this.inmuebles = await this.articuloService.obtenerInmueblesFechas('/InstantAbode/buscarInmuebles', this.fechaInicio, this.fechaFinal, this.provinciaSelec) || [];
    }
    //this.cargados = true;
  }

  logout() {
    this.authService.logout();
    // Redirect to login or do other cleanup
  }

}

