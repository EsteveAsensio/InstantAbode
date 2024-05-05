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
                    this.errorHandler.handleHttpError(data, false, "Obtener Valoraciones");
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Obtener Valoraciones");
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Obtener Valoraciones");
        }
    }

    async modificarValoracionInmueble(tipo: string, valoracion: any): Promise<void | string> {
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
                if (data.status == 200) {
                    return data.result.message;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Modificar Valoraciones");
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Modificar Valoraciones");
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Modificar Valoraciones");
        }
    }

    async addValoracionInmueble(tipo: string, valoracion: any): Promise<void | string> {
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
                if (data.status == 200) {
                    return data.result.message;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Añadir Valoraciones");
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Añadir Valoraciones");
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Añadir Valoraciones");
        }
    }

    async eliminarValoracionInmueble(tipo: string): Promise<void | any> {
        try {
            const data: any = await this.service.deleteUno(tipo).toPromise();
            ///console.log(data)

            if (data) {
                if (data.status == 200) {
                    return data.result.message;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Eliminar Valoraciones");
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Eliminar Valoraciones");
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Eliminar Valoraciones");
        }
    }

}