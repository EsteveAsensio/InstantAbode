import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { SwalAnimation } from '../../utils/SwalAnimation';
import { Usuario } from '../../models/usuario.modelo';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-registrar',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './registrar.component.html',
  styleUrl: './registrar.component.css'
})
export class RegistrarComponent {
  public cliente: Usuario  = {} as Usuario;

  constructor(private router: Router, private authService: AuthService) { }

  cancelar() {
    this.router.navigate(['login'])
  }

  async registrarUsuario() {
    if(this.comprobar()){
      const correcto = await this.authService.registrarUsuario(this.cliente.name, this.cliente.contrasenya,this.cliente.dni,
        this.cliente.nombreCliente,this.cliente.apellidos,this.cliente.correo,this.cliente.telefono, false);
        if(correcto){
          SwalAnimation.showCustomSuccessSwal("Nuevo usuario registrado");
          this.router.navigate(['login'])
        }
    }
  }
  comprobar(): boolean {
    if (!this.cliente.name || this.cliente.name == "") {
      SwalAnimation.showCustomErrorSwal("Error de usuario", "Es necesario indicar el nombre de usuario")
      return false;
    }
    if (!this.cliente.contrasenya || this.cliente.contrasenya == "") {
      SwalAnimation.showCustomErrorSwal("Error de contraseña", "Es necesario indicar la contraseña")
      return false;
    }
    if (!this.cliente.nombreCliente || this.cliente.nombreCliente == "") {
      SwalAnimation.showCustomErrorSwal("Error de cliente", "Es necesario indicar el nombre del cliente")
      return false;
    }
    if (!this.cliente.dni || this.cliente.dni == "") {
      SwalAnimation.showCustomErrorSwal("Error cliente", "Es necesario indicar el DNI")
      return false;
    }
    if (!this.cliente.correo || this.cliente.correo == "") {
      SwalAnimation.showCustomErrorSwal("Error cliente", "Es necesario indicar el correo electrónico")
      return false;
    }
    return true;
  }
}
