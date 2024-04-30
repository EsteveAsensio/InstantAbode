import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth-service';


@Injectable({
  providedIn: 'root',
})
export class HttpInterceptorService implements HttpInterceptor {
  constructor(private authService: AuthService) { }
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Verifica si hay un token de autenticación válido
    const token = this.authService.getAuthToken();
    // Si la solicitud es 'POST users/login', no se agrega ningún encabezado
    if (request.url.endsWith('auth/login')) {
      return next.handle(request);
    }
    // Clona la solicitud original para poder modificarla
    let modifiedHeaders = request.headers;
    if (token) {
      modifiedHeaders = modifiedHeaders.set('Authorization', 'Bearer ' + token);
    }
    // Crear una nueva solicitud con los encabezados modificados
    const modifiedRequest = request.clone({ headers: modifiedHeaders });

    // Continuar con la solicitud modificada
    return next.handle(modifiedRequest);
  }
}

