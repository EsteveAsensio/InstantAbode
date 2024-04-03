import { Component } from '@angular/core';
import { Route, Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Cliente } from '../../models/cliente.modelo';
import { SwalAnimation } from '../../utils/SwalAnimation';

@Component({
  selector: 'app-registrar',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './registrar.component.html',
  styleUrl: './registrar.component.css'
})
export class RegistrarComponent {
  public cliente: Cliente  = {} as Cliente;

  constructor(private router: Router) { }

  cancelar() {
    this.router.navigate(['login'])
  }
  registrarUsuario() {
    if(this.comprobar()){
      this.router.navigate(['login'])
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
