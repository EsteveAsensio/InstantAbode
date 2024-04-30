import { Component } from '@angular/core';
import { GeneralDAO } from '../../services/general.dao';
import { AuthService } from '../../services/auth-service';
import { Inmueble } from '../../models/inmueble.modelo';

@Component({
  selector: 'app-principal',
  standalone: true,
  imports: [],
  templateUrl: './principal.component.html',
  styleUrl: './principal.component.css'
})
export class PrincipalComponent {

   
  constructor(private articuloService: GeneralDAO, private authService: AuthService){}

  /*
  inmuebles: Inmueble[] = [];

  async loadInmuebles() {
   
    this.inmuebles = await this.articuloService.getGeneral('inmuebles') || [];
    //this.cargados = true;
  */

    logout() {
      this.authService.logout();
      // Redirect to login or do other cleanup
    }

}

