import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  constructor() { }

  login(username: string, password: string): void {
    // Aquí iría la lógica para manejar el inicio de sesión
    console.log('Nombre de usuario:', username);
    console.log('Contraseña:', password);
    // Aquí deberías enviar los datos de inicio de sesión al servidor
  }
}
