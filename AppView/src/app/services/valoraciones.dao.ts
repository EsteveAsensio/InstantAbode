import { Injectable } from '@angular/core';

import { BaseService } from './base.service';
import { SwalAnimation } from '../utils/SwalAnimation';
import { AuthService } from './auth-service';
import { ErrorHandlerService } from './errorHandler.service';


@Injectable({
    providedIn: 'root',
})
export class ValoracionesDAO {

    constructor(
        private service: BaseService,
        private errorHandler: ErrorHandlerService,
        private authService: AuthService,
    ) { }

    async obtenerValoracionesUsuario(tipo: string): Promise<void | any[]> {
        try {
            const data: any = await this.service.get(tipo).toPromise();
            ///console.log(data)

            if (data) {
                if (data.status == 200) {
                    return data.valoraciones;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data);
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data);
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error);
        }
    }

    async modificarValoracionInmueble(tipo: string, valoracion: any) {
        try {
            const valoracionData = {
                "id": valoracion.id,
                "comentario": valoracion.comentario,
                "puntuacion": valoracion.puntuacion,
                "fecha": valoracion.fecha
            };
            const data: any = await this.service.put(tipo, valoracionData).toPromise();
            ///console.log(data)

            if (data) {
                if (data.result.status == 200) {
                    return true;
                } else {
                    this.errorHandler.handleHttpError(data);
                    return false;
                }
            } else {
                this.errorHandler.handleHttpError(data);
                return false;
            }
        } catch (error: any) {
            this.errorHandler.handleHttpError(error);
            return true;
        }
    }

    async addValoracionInmueble(tipo: string, valoracion: any){
        try {
            const valoracionData = {
                "id": valoracion.id,
                "comentario": valoracion.comentario,
                "puntuacion": valoracion.puntuacion,
                "fecha": valoracion.fecha,
                "idAlquiler" : valoracion.idAlquiler
            };
            const data: any = await this.service.post(tipo, valoracionData).toPromise();
            ///console.log(data)

            if (data) {
                if (data.result.status == 200) {
                    return true;
                } else {
                    this.errorHandler.handleHttpError(data);
                    return false;
                }
            } else {
                this.errorHandler.handleHttpError(data);
                return false;
            }
        } catch (error: any) {
            this.errorHandler.handleHttpError(error);
            return false;
        }
    }

    async eliminarValoracionInmueble(tipo: string){
        try {
            const data: any = await this.service.deleteUno(tipo).toPromise();
            if (data) {
                if (data.status == 200) {
                    return true;
                } else {
                    this.errorHandler.handleHttpError(data);
                    return false;
                }
            } else {
                this.errorHandler.handleHttpError(data);
                return false;
            }
        } catch (error: any) {
            this.errorHandler.handleHttpError(error);
            return false;
        }
    }

}