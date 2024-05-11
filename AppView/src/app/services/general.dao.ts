
import { Injectable } from '@angular/core';

import { BaseService } from './base.service';
import { SwalAnimation } from '../utils/SwalAnimation';
import { AuthService } from './auth-service';
import { ErrorHandlerService } from './errorHandler.service';




@Injectable({
  providedIn: 'root',
})
export class GeneralDAO {

  constructor(
    private service: BaseService,
    private errorHandler: ErrorHandlerService,
    private authService: AuthService,
  ) { }



  async getLocalUsuario() {
    return this.authService.getUsuario();
  }

  async cambiarPassword(password: string): Promise<boolean> {
    try {
      const data: any = await this.service.cambioDeContrasena('usuarios/cambiarCredenciales', password).toPromise();

      if (data && data.success === 'true') {
        //SwalAnimation.showCustomSuccessSwal('Contraseña cambiada exitosamente');
        return true;
      } else {
        this.errorHandler.handleHttpError(data);
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
    }
    return false;
  }

  async confirmarCodigo(codigo: string): Promise<boolean> {
    try {
      const data: any = await this.service.cambioDeContrasena('usuarios/verificarCodigo', codigo).toPromise();

      if (data && data.success === 'true') {
        // SwalAnimation.showCustomSuccessSwal('Código confirmado exitosamente');
        return true;
      } else {
        this.errorHandler.handleHttpError(data);
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
    }
    return false;
  }

  async enviarCodigo(email: string): Promise<boolean> {
    try {
      const data: any = await this.service.cambioDeContrasena('usuarios/recuperacionEmail', email).toPromise();

      if (data && data.success === 'true') {
        //SwalAnimation.showCustomSuccessSwal('Código de recuperación enviado exitosamente');
        return true;
      } else {
        this.errorHandler.handleHttpError(data);
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
    }
    return false;
  }

  async putGeneral(tipo: string, objeto: any, mensaje: boolean = true): Promise<any> {
    try {

      ////console.log(objeto);
      const data: any = await this.service.put(tipo, objeto).toPromise();
      if (data && !data['error']) {
        if (mensaje)
          SwalAnimation.showCustomSuccessSwal('Actualizado exitosamente');
        return data;
      } else {
        this.errorHandler.handleHttpError(data);
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
    }
  }

  async getGeneral(tipo: string): Promise<void | any[]> {
    try {
      const data: any = await this.service.get(tipo).toPromise();
      if (data && !data.error) {
        return data;
      } else {
        console.log(data)
        this.errorHandler.handleHttpError(data);
        return [];
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
      return [];
    }
  }

  async getGeneralFiltrados(tipo: string, filtro: any): Promise<void | any[]> {
    try {
      const data: any = await this.service.getFiltrados(tipo + '/filtro', filtro).toPromise();
      ////console.log(data)
      if (data && !data.error) {
        return (data);
      } else {
        this.errorHandler.handleHttpError(data);
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
    }
  }


  async postGeneral(tipo: string, objeto: any, mensaje: boolean = true): Promise<any> {
    try {

      const data: any = await this.service.post(tipo, objeto).toPromise();

      if (data && !data.error) {
        if (mensaje)
          SwalAnimation.showCustomSuccessSwal('Creado exitosamente');
        return data;

      } else {
        this.errorHandler.handleHttpError(data);
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
    }
  }

  async deleteGeneral(tipo: string, objeto: any): Promise<any> {
    try {
      const data: any = await this.service.delete(tipo + "/" + objeto.id, objeto).toPromise();
      ////console.log(data)
      if (data && !data.error) {
        SwalAnimation.showCustomSuccessSwal('Eliminado exitosamente');
        return data;
      } else {
        this.errorHandler.handleHttpError(data);
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error);
    }

  }
}
