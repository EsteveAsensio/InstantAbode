import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { GeneralDAO } from '../../services/general.dao';
import { AuthService } from '../../services/auth-service';
import { Inmueble } from '../../models/inmueble.modelo';
import { InmuebleDAO } from '../../services/inmuebles.dao';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-informacion-inmueble',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent, RouterModule],
  templateUrl: './informacion-inmueble.component.html',
  styleUrl: './informacion-inmueble.component.css'
})
export class InformacionInmuebleComponent implements OnInit {
  inmueble: any;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer,
    private inmueblesService: InmuebleDAO,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = params['id'];
      this.cargarInmueble(id);
    });
  }

  async cargarInmueble(id: string) {
    this.inmueble = await this.inmueblesService.obtenerInfoInmueble('InstantAbode/infoInmueble/' + id);
  }
  
  sanitizeImageUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }
}
