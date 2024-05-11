import { Component } from '@angular/core';
import { GeneralDAO } from '../../services/general.dao';
import { AuthService } from '../../services/auth-service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { InmuebleDAO } from '../../services/inmuebles.dao';
import { Usuario } from '../../models/usuario.modelo';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { Alquiler } from '../../models/alquiler.modelo';
import { DomSanitizer } from '@angular/platform-browser';
import { MatDialog } from '@angular/material/dialog';
import { InfoValoracioninmuebleComponent } from '../info-valoracioninmueble/info-valoracioninmueble.component';
import { SwalAnimation } from '../../utils/SwalAnimation';
import { Router } from '@angular/router';
import { ValoracionesDAO } from '../../services/valoraciones.dao';

@Component({
  selector: 'app-inmuebles-alquilados',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  templateUrl: './inmuebles-alquilados.component.html',
  styleUrl: './inmuebles-alquilados.component.css'
})
export class InmueblesAlquiladosComponent {
  constructor(private valoDAO: ValoracionesDAO, private router: Router, public dialog: MatDialog,
    private sanitizer: DomSanitizer, private articuloService: GeneralDAO, private inmueblesService: InmuebleDAO, private authService: AuthService) { }
  alquileres: Alquiler[] = [];
  usuario: Usuario = {} as Usuario;

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
    this.alquileres = await this.inmueblesService.obtenerInmueblesAlquilados('InstantAbode/inmueblesAlquilados/' + this.usuario.id) || [];
  }

  sanitizeImageUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }

  async eliminarValoracion(idValoracion: number) {
    const confirm = await SwalAnimation.showConfirmDeleteMessageSwal();
    if (confirm) {
      const eliminar = await this.valoDAO.eliminarValoracionInmueble("InstantAbode/eliminarValoracionInmueble/" + idValoracion);
      if (eliminar){
        SwalAnimation.showCustomSuccessSwal("Valoración eliminada con éxito.");
        this.router.navigateByUrl('/RefreshComponent', { skipLocationChange: true }).then(() => {
          this.router.navigate(['inmuebles-alquilados']);
        });
      }
    }
  }

  openDialog(alquiler: Alquiler): void {
    const dialogRef = this.dialog.open(InfoValoracioninmuebleComponent, {
      width: '400px',
      data: { valoracion: alquiler.valoracionInmueble || { comentario: '', puntuacion: 0, fecha: new Date(), idAlquiler: alquiler.id } }
    });
    dialogRef.afterClosed().subscribe(result => {
      this.router.navigateByUrl('/RefreshComponent', { skipLocationChange: true }).then(() => {
        this.router.navigate(['inmuebles-alquilados']);
      });
    });
  }
}
