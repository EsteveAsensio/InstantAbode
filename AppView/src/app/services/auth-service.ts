import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import * as CryptoJS from 'crypto-js';

import { Router } from '@angular/router';
import { URL_BACKEND } from './constantesHTTP';

import { Cliente } from '../models/cliente.modelo';
import { BaseService } from './base.service';


const jsog = new JsogService();

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly baseUrl = URL_BACKEND;
  private authToken: string | null = null;
  private encryptedKey = 'Oberta2022**';
  private static encryptedKey = 'Oberta2022**';
  constructor(private http: HttpClient, private router: Router, private service: BaseService, private errorHandler: ErrorHandlerService) { }

  async login(username: string, password: string, sesionIniciada: boolean) {
    const loginData = { username, password };
    try {
      var data: any = await this.service.post('auth/login', loginData).toPromise();
      if (data) {
        data = jsog.deserialize(data);
        this.authToken = data.token;
        var empresa = data.usuario.empresa as Empresa;
        var usuario = data.usuario as Usuario;
        usuario.roles = [];
        for (let rol of data.usuario.authorities) {
          usuario.roles.push(new Rol(0, rol.authority, "#456456"));
        }
        const userAgent = navigator.userAgent;
        const esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
        if (!usuario.propiedades) {
          usuario.propiedades = {};
        } else {
          usuario.propiedades = JSON.parse(usuario.propiedades)
        }
        if (esMovil) {
          usuario.propiedades.telefono = true;
        } else {
          usuario.propiedades.telefono = false;
        }

        sessionStorage.setItem('encryptedToken', this.encryptData(this.authToken, this.encryptedKey));
        sessionStorage.setItem('encryptedEmpresa', this.encryptData(JSON.stringify(jsog.serialize(empresa)), this.encryptedKey));
        sessionStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(jsog.serialize(usuario)), this.encryptedKey));

        if (sesionIniciada) {
          localStorage.setItem('encryptedToken', this.encryptData(this.authToken, this.encryptedKey));
          localStorage.setItem('encryptedEmpresa', this.encryptData(JSON.stringify(jsog.serialize(empresa)), this.encryptedKey));
          localStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(jsog.serialize(usuario)), this.encryptedKey));
        }

        this.controladorDepPaginas();
      } else {
        ////console.log(data)
        this.errorHandler.handleHttpError(data,false,"login");
      }
    } catch (error: any) {
      ////console.log(error)
      this.errorHandler.handleHttpError(error,false,"login");
    }
    return false;

  }

  controladorDepPaginas() {
    if (this.hasRole('ADMIN')) {
      this.router.navigateByUrl('escritorio');
    } else {
      this.router.navigateByUrl('escritorio');
    }
  }

  confirmarTerminosYServicios() {
    return this.http.post(`${this.baseUrl}login/terminos`, null).pipe(
      tap(() => {
        var usuario: Usuario = this.getUsuario() || {} as Usuario;
        //////////console.log((usuario);

        usuario.condicionesaceptadas = true;
        sessionStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(usuario), this.encryptedKey));
      })
    );
  }


  async guardarFiltrosPedidos(filtropedidos: any) {
    //console.log("Paso 6.2")
    sessionStorage.setItem('encryptedFiltroPedidos', this.encryptData(JSON.stringify(jsog.serialize(filtropedidos)), this.encryptedKey));
  }
  async getFiltrosPedidos(): Promise<any> {
    const encryptedFiltroPedidos = sessionStorage.getItem('encryptedFiltroPedidos');
    var filtroPedidos: any = encryptedFiltroPedidos ? this.decryptData(encryptedFiltroPedidos, this.encryptedKey) : null;
    return jsog.deserialize(JSON.parse(filtroPedidos));
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

  async delOfCarrito(articulo: Articulo) {
    const carrito: Carrito = await this.getCarrito() || new Carrito([]);

    // Usar findIndex para encontrar el índice del objeto que coincide con el artículo.
    const indexToRemove = carrito.articulos.findIndex(objeto => objeto.articulo_id === articulo.id);

    if (indexToRemove !== -1) {
      const objeto = carrito.articulos[indexToRemove];
      objeto.cantidad -= 1;

      if (objeto.cantidad === 0) {
        // Si la cantidad llega a cero, eliminar el objeto.
        carrito.articulos.splice(indexToRemove, 1);
      }

      // Actualizar el carrito en la sesión de almacenamiento.
      var usuario: Usuario = this.getUsuario()!
      usuario.carrito = JSON.stringify(carrito);
      sessionStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(usuario), this.encryptedKey));
      this.service.put('usuarios/carrito', JSON.stringify(carrito)).toPromise();
    }
  }

  async addToCarrito(articulo: Articulo) {
    const carrito: Carrito = await this.getCarrito() || new Carrito([]);
    const objetoEnCarrito = carrito.articulos.find(objeto => objeto.articulo_id === articulo.id);

    if (objetoEnCarrito) {
      objetoEnCarrito.cantidad += 1;
    } else {
      carrito.articulos.push(new ObjetoCarrito(articulo.id, 1));
    }
    ////console.log(carrito)

    var usuario: Usuario = this.getUsuario()!
    usuario.carrito = JSON.stringify(carrito);
    sessionStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(usuario), this.encryptedKey));
    this.service.put('usuarios/carrito', JSON.stringify(carrito)).toPromise();
  }

  async refreshCarrito(carrito: Carrito) {
    var usuario: Usuario = this.getUsuario()!
    usuario.carrito = JSON.stringify(carrito);
    sessionStorage.setItem('encryptedUsuario', this.encryptData(JSON.stringify(usuario), this.encryptedKey));
    await this.service.put('usuarios/carrito', JSON.stringify(carrito)).toPromise();
  }
  saveInstantObject(object: any) {
    sessionStorage.setItem('encryptedMomentObject', this.encryptData(JSON.stringify(jsog.serialize(object)), this.encryptedKey));
  }
  getInstantObject() {
    var encryptObject: string | null = sessionStorage.getItem('encryptedMomentObject');
    sessionStorage.removeItem('encryptedMomentObject')
    if (encryptObject) {
      const decryptedObject = jsog.deserialize(JSON.parse(this.decryptData(encryptObject, this.encryptedKey)));
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



  getUser(): Usuario | null {
    const encryptedUsuario = this.getencryptedUsuario();
    if (encryptedUsuario) {
      const decryptedUser = this.decryptData(encryptedUsuario, this.encryptedKey);
      const user = jsog.deserialize(JSON.parse(decryptedUser)) as Usuario;
      return user;
    }
    return null;
  }

  async getCarrito(): Promise<Carrito | null> {
    const encryptedUsuario = this.getencryptedUsuario();
    if (encryptedUsuario) {
      const decryptedUsuario = this.decryptData(encryptedUsuario, this.encryptedKey);
      const Usuario = jsog.deserialize(JSON.parse(decryptedUsuario)) as Usuario;
      if (Usuario.carrito) {
        return JSON.parse(Usuario.carrito);
      }
    }
    return null;
  }

  getEmpresa(): Empresa | null {
    const encryptedEmpresa = this.getEncryptedEmpresa();
    if (encryptedEmpresa) {
      const decryptedEmpresa = this.decryptData(encryptedEmpresa, this.encryptedKey);
      const empresa = jsog.deserialize(JSON.parse(decryptedEmpresa)) as Empresa;
      return empresa;
    }
    return null;
  }

  static getEmpresa(): Empresa | null {
    const encryptedEmpresa = this.getEncryptedEmpresa();
    if (encryptedEmpresa) {
      const decryptedEmpresa = this.decryptData(encryptedEmpresa, this.encryptedKey);
      const empresa = jsog.deserialize(JSON.parse(decryptedEmpresa)) as Empresa;
      return empresa;
    }
    return null;
  }

  getUsuario(): Usuario | null {
    const encryptedUsuario = this.getencryptedUsuario();
    if (encryptedUsuario) {
      const decryptedUsuario = this.decryptData(encryptedUsuario, this.encryptedKey);
      const Usuario = jsog.deserialize(JSON.parse(decryptedUsuario)) as Usuario;
      return Usuario;
    }
    return null;
  }

  getUsuarioStrPropiedades(): Usuario | null {
    const encryptedUsuario = this.getencryptedUsuario();
    if (encryptedUsuario) {
      const decryptedUsuario = this.decryptData(encryptedUsuario, this.encryptedKey);
      const Usuario = jsog.deserialize(JSON.parse(decryptedUsuario)) as Usuario;
      Usuario.propiedades = JSON.stringify(Usuario.propiedades);
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
    const usuario = this.getUser();
    if (usuario) {
      for (const rolUsuario of usuario.roles) {
        if (rolUsuario.name.toString().toLowerCase() == rol.toLowerCase()) {
          return true;
        }
      }
    }
    return false;
  }
}
