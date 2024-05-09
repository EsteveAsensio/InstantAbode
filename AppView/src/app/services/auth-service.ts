import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { tap } from 'rxjs/operators';
import * as CryptoJS from 'crypto-js';

import { Router } from '@angular/router';

import { BaseService } from './base.service';
import { Usuario } from '../models/usuario.modelo';
import { URL_BACKEND } from './constantesHTTP';
import { ErrorHandlerService } from './errorHandler.service';
import { OdooAuthResponse } from '../interface/odoo.interfaces';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly baseUrl = URL_BACKEND;
  private authToken: string | null = null;
  private encryptedKey = 'aaaaa';
  private static encryptedKey = 'aaaaa';
  constructor(private http: HttpClient, private router: Router, private service: BaseService, private errorHandler: ErrorHandlerService) { }

  loginOdoo(username: string, password: string) {
    const body = {
      jsonrpc: "2.0",
      params: {
        db: "InstantAbode",
        login: username,
        password: password
      }
    };
  
    return this.http.post<OdooAuthResponse>(`${this.baseUrl}/web/session/authenticate`, body)
      .pipe(
        tap(response => {
          if (response && response.result && response.result.session_id) {
            const sessionId = response.result.session_id;
            console.log(response)
            localStorage.setItem('odoo_session_id', sessionId);  // Guardar session_id
          }
        }),
        catchError(error => {
          console.log(error)
          console.error('Error during Odoo authentication:', error);
          return throwError(() => error);  // Propaga el error para manejo externo
        })
      );
  }


  async login(username: string, password: string, sesionIniciada: boolean) {
    const loginData = {
      "username": username,
      "contrasenya": password
    };
    try {
      var data: any = await this.service.post('InstantAbode/login', loginData).toPromise();
      ///console.log(data)
      if (data.result) {

        if (data.result.status == 200) {

          this.authToken = data.token;
          var usuario = data.result.usuario as Usuario;

          sessionStorage.setItem('encryptedToken', this.encryptData(this.authToken, this.encryptedKey));
          sessionStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(usuario), this.encryptedKey));
          if (sesionIniciada) {
            localStorage.setItem('encryptedToken', this.encryptData(this.authToken, this.encryptedKey));
            localStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(usuario), this.encryptedKey));
          }

          this.controladorDepPaginas();
        } else {
          ////console.log(data)
          this.errorHandler.handleHttpError(data, false, "login");
        }
      } else {
        ////console.log(data)
        this.errorHandler.handleHttpError(data, false, "login");
      }
    } catch (error: any) {
      ////console.log(error)
      this.errorHandler.handleHttpError(error, false, "login");
    }
    return false;

  }

  async registrarUsuario(username: string, password: string, dni: string, nombre: string, apellidos: string, correo: string, telefono: number, sesionIniciada: boolean) {
    const registrarData = {
      "name": username,
      "apellidos": apellidos,
      "dni": dni,
      "nombreCliente": nombre,
      "correo": correo,
      "contrasenya": password,
      "telefono": telefono
    };
    try {
      var data: any = await this.service.post('InstantAbode/registrarNuevoUsuario', registrarData).toPromise();
      console.log(data)
      if (data.result) {

        if (data.result.status == 200) {

        } else {
          ////console.log(data)
          this.errorHandler.handleHttpError(data, false, "Registrar Usuario");
        }
      } else {
        ////console.log(data)
        this.errorHandler.handleHttpError(data, false, "Registrar Usuario");
      }
    } catch (error: any) {
      ////console.log(error)
      this.errorHandler.handleHttpError(error, false, "Registrar Usuario");
    }
    return false;
  }

  async modificarCliente(user : Usuario) {
    const registrarData = {
      "id": user.id,
      "name": user.name,
      "apellidos": user.apellidos,
      "dni": user.apellidos,
      "nombreCliente": user.nombreCliente,
      "correo": user.correo,
      "contrasenya": user.contrasenya,
      "telefono": user.telefono,
      "imagen": user.imagen
    };
    try {
      var data: any = await this.service.put('InstantAbode/modificarCliente', registrarData).toPromise();
      ///console.log(data)
      if (data.result) {
        if (data.result.status == 200) {
          return true;
        } else {
          this.errorHandler.handleHttpError(data, false, "Modificar Usuario");
        }
      } else {
        this.errorHandler.handleHttpError(data, false, "Modificar Usuario");
      }
    } catch (error: any) {
      this.errorHandler.handleHttpError(error, false, "Modificar Usuario");
    }
    return false;
  }

  controladorDepPaginas() {

    this.router.navigateByUrl('principal');

  }


  logout(): void {
    this.authToken = null;

    localStorage.removeItem('encryptedToken');
    localStorage.removeItem('encryptedUsuario');
    localStorage.removeItem('encryptedEmpresa');

    sessionStorage.removeItem('encryptedToken');
    sessionStorage.removeItem('encryptedUsuario');
    sessionStorage.removeItem('encryptedEmpresa');
    sessionStorage.removeItem('encryptedEjercicio');
    this.eliminarModoSeguro();
    this.router.navigateByUrl('/login');

  }


  static logout(): void {


    localStorage.removeItem('encryptedToken');
    localStorage.removeItem('encryptedUsuario');
    localStorage.removeItem('encryptedEmpresa');


    sessionStorage.removeItem('encryptedToken');
    sessionStorage.removeItem('encryptedUsuario');
    sessionStorage.removeItem('encryptedEmpresa');
    sessionStorage.removeItem('encryptedEjercicio');
    sessionStorage.removeItem('passwordModoSeguro');
    sessionStorage.removeItem('codigoModoSeguro');
  }

  eliminarModoSeguro() {
    sessionStorage.removeItem('passwordModoSeguro');
    sessionStorage.removeItem('codigoModoSeguro');
  }

  getAuthToken(): string | null {

    const encryptedToken = sessionStorage.getItem('encryptedToken');
    const encryptedTokenlocal = localStorage.getItem('encryptedToken');
    this.authToken = encryptedToken ? this.decryptData(encryptedToken, this.encryptedKey) : (encryptedTokenlocal ? this.decryptData(encryptedTokenlocal, this.encryptedKey) : null);

    return this.authToken;
  }


  saveInstantObject(object: any) {
    sessionStorage.setItem('encryptedMomentObject', this.encryptData(JSON.stringify(object), this.encryptedKey));
  }
  getInstantObject() {
    var encryptObject: string | null = sessionStorage.getItem('encryptedMomentObject');
    sessionStorage.removeItem('encryptedMomentObject')
    if (encryptObject) {
      const decryptedObject = JSON.parse(this.decryptData(encryptObject, this.encryptedKey));
      return decryptedObject;
    }
    return null;


  }
  getencryptedUsuario(): string | null {
    return sessionStorage.getItem('encryptedUsuario') || localStorage.getItem('encryptedUsuario');
  }

  getencryptedCarrito(): string | null {
    return sessionStorage.getItem('encryptedCarrito') || localStorage.getItem('encryptedCarrito');
  }

  // Se asume que esta debería ser una función no estática, dado el contexto de las demás funciones
  static getencryptedUsuario(): string | null {
    return sessionStorage.getItem('encryptedUsuario') || localStorage.getItem('encryptedUsuario');
  }

  getEncryptedEmpresa(): string | null {
    return sessionStorage.getItem('encryptedEmpresa') || localStorage.getItem('encryptedEmpresa');
  }

  static getEncryptedEmpresa(): string | null {
    return sessionStorage.getItem('encryptedEmpresa') || localStorage.getItem('encryptedEmpresa');
  }

  getEncryptedEjercicio(): string | null {
    return sessionStorage.getItem('encryptedEjercicio') || localStorage.getItem('encryptedEjercicio');
  }

  getEncryptedToken(): string | null {
    return sessionStorage.getItem('encryptedToken') || localStorage.getItem('encryptedToken');
  }

  getEncryptedCodigoModoSeguro(): string | null {
    return sessionStorage.getItem('codigoModoSeguro') || localStorage.getItem('codigoModoSeguro');
  }

  getEncryptedPasswordModoSeguro(): string | null {
    return sessionStorage.getItem('passwordModoSeguro') || localStorage.getItem('passwordModoSeguro');
  }


  getUsuario(): Usuario | null {
    const encryptedUsuario = this.getencryptedUsuario();
    if (encryptedUsuario) {
      const decryptedUsuario = this.decryptData(encryptedUsuario, this.encryptedKey);
      const Usuario = JSON.parse(decryptedUsuario) as Usuario;
      return Usuario;
    }
    return null;
  }

  getUsuarioStrPropiedades(): Usuario | null {
    const encryptedUsuario = this.getencryptedUsuario();
    if (encryptedUsuario) {
      const decryptedUsuario = this.decryptData(encryptedUsuario, this.encryptedKey);
      const Usuario = JSON.parse(decryptedUsuario) as Usuario;
      return Usuario;
    }
    return null;
  }


  getCodigoModoSeguro(): string | null {
    const encryptedUsuario = this.getEncryptedCodigoModoSeguro();
    if (encryptedUsuario) {
      const decryptedUsuario = this.decryptData(encryptedUsuario, this.encryptedKey);
      const Usuario = decryptedUsuario;
      return Usuario;
    }
    return null;
  }

  getPasswordSeguro(): string | null {
    const encryptedUsuario = this.getEncryptedPasswordModoSeguro();
    if (encryptedUsuario) {
      const decryptedUsuario = this.decryptData(encryptedUsuario, this.encryptedKey);
      const Usuario = decryptedUsuario;
      return Usuario;
    }
    return null;
  }


  // getEjercicio(): Ejercicio | null {
  //   const encryptedEjercicio = this.getEncryptedEjercicio();
  //   if (encryptedEjercicio) {
  //     const decryptedEjercicio = this.decryptData(encryptedEjercicio, this.encryptedKey);
  //     const Ejercicio = JSON.parse(decryptedEjercicio) as Ejercicio;
  //     return Ejercicio;
  //   }
  //   return null;
  // }



  async setPasswordModoSeguro(codigo: string) {
    sessionStorage.setItem('passwordModoSeguro', this.encryptData(codigo, this.encryptedKey));
    return true;
  }
  async setCodigoModoSeguro(codigo: string) {
    sessionStorage.setItem('codigoModoSeguro', this.encryptData(codigo, this.encryptedKey));
    return true;
  }






  isLoggedIn(): boolean {
    return !!this.getAuthToken();
  }

  private encryptData(data: any, key: string): string {
    try {
      const encryptedData = CryptoJS.AES.encrypt(data, key).toString();
      return encryptedData;
    } catch (e) {
      this.logout();
      return '';
    }


  }

  private decryptData(encryptedData: string, key: string): string {
    try {
      const decryptedData = CryptoJS.AES.decrypt(encryptedData, key).toString(CryptoJS.enc.Utf8);
      return decryptedData;
    } catch (e) {
      this.logout();
      return '';
    }
  }
  private static decryptData(encryptedData: string, key: string): string {
    try {
      const decryptedData = CryptoJS.AES.decrypt(encryptedData, key).toString(CryptoJS.enc.Utf8);
      return decryptedData;
    } catch (e) {
      this.logout();
      return '';
    }
  }

  hasToken(): boolean {
    const token = this.getAuthToken();
    if (token && token.length > 0) {
      return true;
    }
    return false;
  }

  esTelefonoMovil() {
    const userAgent = navigator.userAgent;
    const esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
    if (esMovil) {
      return true;
    } else {
      return false;
    }

  }

  hasRole(rol: string): boolean {
    const usuario = this.getUsuario();
    if (usuario) {
      if (usuario.rol.toLowerCase() == rol.toLowerCase()) {
        return true;
      }
    }
    return false;
  }
}
