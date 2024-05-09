import { Component } from '@angular/core';
import { Usuario } from '../../models/usuario.modelo';
import { FormsModule } from '@angular/forms';
import { GeneralDAO } from '../../services/general.dao';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { CommonModule } from '@angular/common';
import { Route, Router, RouterModule } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { SwalAnimation } from '../../utils/SwalAnimation';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-perfil-usuario',
  standalone: true,
  imports: [FormsModule, CommonModule, SidebarComponent],
  templateUrl: './perfil-usuario.component.html',
  styleUrl: './perfil-usuario.component.css'
})
export class PerfilUsuarioComponent {
  public usuario: Usuario = {} as Usuario;

  constructor(private authService: AuthService, private sanitizer: DomSanitizer, private router: Router, private articuloService: GeneralDAO) { }

  ngOnInit(): void {
    this.loadUserData();
  }

  cancelar() {
    this.router.navigate(['principal'])
  }

  private async loadUserData(): Promise<void> {
    const usuario = await this.articuloService.getLocalUsuario();
    if (usuario !== null) {
      this.usuario = usuario;
    }
  }

  async actualizar(): Promise<void> {
    if (this.comprobar()) {
      this.authService.modificarCliente(this.usuario)
    }
  }

  comprobar(): boolean {
    if (!this.usuario.name || this.usuario.name == "") {
      SwalAnimation.showCustomErrorSwal("Error de usuario", "Es necesario indicar el nombre de usuario")
      return false;
    }
    if (!this.usuario.contrasenya || this.usuario.contrasenya == "") {
      SwalAnimation.showCustomErrorSwal("Error de contraseña", "Es necesario indicar la contraseña")
      return false;
    }
    if (!this.usuario.nombreCliente || this.usuario.nombreCliente == "") {
      SwalAnimation.showCustomErrorSwal("Error de cliente", "Es necesario indicar el nombre del cliente")
      return false;
    }
    if (!this.usuario.dni || this.usuario.dni == "") {
      SwalAnimation.showCustomErrorSwal("Error cliente", "Es necesario indicar el DNI")
      return false;
    }
    if (!this.usuario.correo || this.usuario.correo == "") {
      SwalAnimation.showCustomErrorSwal("Error cliente", "Es necesario indicar el correo electrónico")
      return false;
    }
    return true;
  }

  onFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length > 0) {
      const file = files[0];
      const reader = new FileReader();
      reader.onload = (e: any) => {
        const base64Image = e.target.result;
        console.log("Base64 image data:", base64Image); // Log original base64 data

        // Eliminar el prefijo 'data:image/jpeg;base64,' antes de guardar
        const base64Data = base64Image.split(',')[1];
        if (!base64Data) {
          console.error("Error procesando la imagen en base64.");
          return;
        }

        this.usuario.imagen = base64Data;
        console.log("Processed Base64 Data:", this.usuario.imagen); // Log processed base64 data
      };
      reader.readAsDataURL(file);
    }
  }



  sanitizeImageUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }


}
