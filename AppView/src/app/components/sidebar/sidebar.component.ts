import { Component } from '@angular/core';
import { AuthService } from '../../services/auth-service';
import { GeneralDAO } from '../../services/general.dao';
import { Usuario } from '../../models/usuario.modelo';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent {
  public usuario: Usuario = {} as Usuario;
  constructor(private router: Router, private articuloService: GeneralDAO, private authService: AuthService, private sanitizer: DomSanitizer) { }

  logout() {
    this.authService.logout();
  }
  ngOnInit(): void {
    this.loadUserData();
  }

  private async loadUserData(): Promise<void> {
    const usuario = await this.articuloService.getLocalUsuario();
    if (usuario !== null) {
      this.usuario = usuario;
    }
  }
  sanitizeImageUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }
  navigate(route: string) {
    this.router.navigateByUrl('/RefreshComponent')
    this.router.navigateByUrl(route);
  }
}
