import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class OdooInterceptor implements HttpInterceptor {
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const sessionId = localStorage.getItem('odoo_session_id');
        if (sessionId) {
            // Añadir el session_id a las cabeceras de la solicitud
            const clonedRequest = req.clone({
                headers: req.headers.set('Cookie', `session_id=${sessionId}`)
            });
            return next.handle(clonedRequest);
        }
        return next.handle(req);
    }
}
