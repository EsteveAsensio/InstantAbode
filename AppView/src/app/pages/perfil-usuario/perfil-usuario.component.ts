import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { AuthService } from '../../services/auth-service';
import { GeneralDAO } from '../../services/general.dao';
import { SwalAnimation } from '../../utils/SwalAnimation';
import { Usuario } from '../../models/usuario.modelo';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-perfil-usuario',
  standalone: true,
  imports: [FormsModule, SidebarComponent],
  templateUrl: './perfil-usuario.component.html',
  styleUrls: ['./perfil-usuario.component.css']
})
export class PerfilUsuarioComponent {
  public usuario: Usuario = {} as Usuario;
  public selectedFile: File | null = null;

  constructor(
    private authService: AuthService,
    private sanitizer: DomSanitizer,
    private router: Router,
    private articuloService: GeneralDAO,
    private http: HttpClient
  ) { }

  ngOnInit(): void {
    this.loadUserData();
  }

  async loadUserData(): Promise<void> {
    const usuario = await this.articuloService.getLocalUsuario();
    if (usuario !== null) {
      this.usuario = usuario;
    }
  }


  onFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length > 0) {
      this.selectedFile = files[0];
      this.encodeImageFileAsURL(this.selectedFile);
    }
  }

  encodeImageFileAsURL(file: File): void {
    const reader = new FileReader();
    reader.onload = (event: any) => {
      const base64Image = event.target.result;
      const base64Data = base64Image.split(',')[1];
      this.usuario.imagen = base64Data;
    };
    reader.onerror = error => console.error("Error al leer el archivo: ", error);
    reader.readAsDataURL(file);
  }

  async actualizar(): Promise<void> {
    if (this.comprobar()) {
      const resultado = await this.authService.modificarCliente(this.usuario);
      if (resultado) {
        SwalAnimation.showCustomSuccessSwal("Perfil Actualizado");
        await this.loadUpdatedUserData();  // Carga los datos actualizados
        this.router.navigate(['perfil-usuario']); // Re-carga la vista de perfil para reflejar los cambios
      }
    }
  }
  
  async loadUpdatedUserData(): Promise<void> {
    const updatedUsuario = await this.authService.getUsuarioActualizado(this.usuario.id);
    if (updatedUsuario) {
      this.usuario = updatedUsuario;
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

  cancelar(): void {
    this.router.navigate(['principal']);
  }

  sanitizeImageUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }
}
