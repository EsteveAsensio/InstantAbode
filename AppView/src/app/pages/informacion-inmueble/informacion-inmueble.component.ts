import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { Inmueble } from '../../models/inmueble.modelo';
import { InmuebleDAO } from '../../services/inmuebles.dao';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { RouterModule } from '@angular/router';
import { DatosTarjetaComponent } from '../datos-tarjeta/datos-tarjeta.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-informacion-inmueble',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent, RouterModule],
  templateUrl: './informacion-inmueble.component.html',
  styleUrl: './informacion-inmueble.component.css'
})
export class InformacionInmuebleComponent implements OnInit {
  inmueble: any;
  fechaInicio: Date | null = null;
  fechaFinal: Date | null = null;
  diasAlquiler: number = 0;
  precioAlquiler: number = 0;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer,
    private inmueblesService: InmuebleDAO,
    public dialog: MatDialog,
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = params['id'];
      this.fechaInicio = new Date(params['fechaInicio']);
      this.fechaFinal = new Date(params['fechaFinal']);

      if (this.fechaInicio && this.fechaFinal) {
        const diffTime = Math.abs(this.fechaFinal.getTime() - this.fechaInicio.getTime());
        this.diasAlquiler = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); // Convierte de milisegundos a días
      }

      this.cargarInmueble(id);
    });
  }

  async cargarInmueble(id: string) {
    this.inmueble = await this.inmueblesService.obtenerInfoInmueble('InstantAbode/infoInmueble/' + id);
    if (this.inmueble && this.diasAlquiler) {
      this.inmueble.fechaInicio = this.fechaInicio;
      this.inmueble.fechaFinal = this.fechaFinal;
      this.precioAlquiler = this.diasAlquiler * this.inmueble.precio;
    }
  }

  sanitizeImageUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }

  openDialog(inmuele: Inmueble): void {
    const dialogRef = this.dialog.open(DatosTarjetaComponent, {
      width: '500px',
      data: inmuele
    });
  }

  cambiarImagenPrincipal(index: number): void {
    const imagenSeleccionada = this.inmueble.imagenes[index];

    this.inmueble.imagenes.push(this.inmueble.imagenPrincipal);
    this.inmueble.imagenPrincipal = imagenSeleccionada;
    this.inmueble.imagenes.splice(index, 1);
}
}
