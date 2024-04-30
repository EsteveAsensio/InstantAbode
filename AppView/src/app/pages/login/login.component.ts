import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Route, Router, RouterModule } from '@angular/router';
import { SwalAnimation } from '../../utils/SwalAnimation';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  public username: string = '';
  public password: string = '';


constructor(private router: Router, private authService: AuthService){}

  registrar(){
    this.router.navigate(['registrar'])
  }

  login(){
    if(this.comprobar()){
      this.authService.login(this.username, this.password, true);
    }
  }

  comprobar(): boolean {
    if (!this.username || this.username == "") {
      SwalAnimation.showCustomErrorSwal("Error de usuario", "Es necesario indicar el nombre de usuario")
      return false;
    }
    if (!this.password || this.password == "") {
      SwalAnimation.showCustomErrorSwal("Error de contraseña", "Es necesario indicar la contraseña")
      return false;
    }
    return true;
  }
}
