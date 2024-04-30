import { Injectable } from '@angular/core';
import { SwalAnimation } from '../utils/SwalAnimation';
import { Router } from '@angular/router';



@Injectable({
    providedIn: 'root'
})
export class ErrorHandlerService {
    constructor(private router: Router) { }

    handleHttpPassword() {
        SwalAnimation.showCustomErrorSwal('Error', "Contraseña incorrecta");
    }

    async handleHttpError(error: any, isDelete: boolean = false, procedencia: string = '') {
        if (error.result) {
            if (error.result.status != 200) {
                await SwalAnimation.showCustomWarningMessageSwal("Error " + error.result.status, error.result.message);
                this.logout();
            }
        } else {
            await SwalAnimation.showCustomWarningMessageSwal("Error " + error.result.status, error.result.message);
            this.logout();
        }


    }
    handleUnauthorizedError(procedencia: string = ''): void {
        if (procedencia == "login") {
            SwalAnimation.showCustomWarningMessageSwal('Contraseña o usuario incorrecto', 'La contraseña o el usuario es incorrecto');
        } else {
            SwalAnimation.showCustomWarningMessageSwal('Se ha cerrado la sesión', 'El tiempo de sesión se ha acabado o se ha entrado en esta cuenta desde otro dispositivo');
        }

        this.logout();
    }

    logout(): void {
        sessionStorage.removeItem('encryptedToken');
        sessionStorage.removeItem('encryptedUsuario');
        sessionStorage.removeItem('encryptedEmpresa');
        localStorage.removeItem('encryptedToken');
        localStorage.removeItem('encryptedUsuario');
        localStorage.removeItem('encryptedEmpresa');
        sessionStorage.removeItem('encryptedEjercicio');
        //this.eliminarModoSeguro();
        this.router.navigateByUrl('/login');

    }
}