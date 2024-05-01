import { Component } from '@angular/core';
import { GeneralDAO } from '../../services/general.dao';
import { AuthService } from '../../services/auth-service';
import { Inmueble } from '../../models/inmueble.modelo';
import { FormsModule } from '@angular/forms';
import { CommonModule  } from '@angular/common';
import { InmuebleDAO } from '../../services/inmuebles.dao';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  templateUrl: './principal.component.html',
  styleUrl: './principal.component.css'
})
export class PrincipalComponent {


  constructor(private articuloService: GeneralDAO, private inmueblesService: InmuebleDAO,private authService: AuthService) { }

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
      this.inmuebles = await this.inmueblesService.obtenerInmueblesFechas('/InstantAbode/buscarInmuebles', this.fechaInicio, this.fechaFinal, this.provinciaSelec) || [];
    }
  }

}

