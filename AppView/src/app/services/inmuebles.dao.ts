
import { Injectable } from '@angular/core';

import { BaseService } from './base.service';
import { SwalAnimation } from '../utils/SwalAnimation';
import { AuthService } from './auth-service';
import { ErrorHandlerService } from './errorHandler.service';


@Injectable({
    providedIn: 'root',
})
export class InmuebleDAO {

    constructor(
        private service: BaseService,
        private errorHandler: ErrorHandlerService,
        private authService: AuthService,
    ) { }

    async obtenerInmueblesFechas(tipo: string, fechaInicio: Date, fechaFinal: Date, provincia: String) {
        try {
            const inmuebleData = {
                "provincia": provincia,
                "fechaInicio": fechaInicio,
                "fechaFinal": fechaFinal
            };
            const data: any = await this.service.post(tipo, inmuebleData).toPromise();
            //console.log(data);

            if (data.result) {
                if (data.result.status == 200) {
                    return data.result.inmuebles;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Obtener Inmuebles");
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Obtener Inmuebles");
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Obtener Inmuebles");
        }
    }

    async obtenerInmueblesAlquilados(tipo: string): Promise<void | any[]> {
        try {
            const data: any = await this.service.get(tipo).toPromise();
            console.log(data)

            if (data) {
                if (data.status == 200) {
                    return data.inmuebles;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Obtener Alquileres");
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Obtener Alquileres");
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Obtener Alquileres");
        }
    }

    async obtenerInfoInmueble(tipo: string): Promise<void | any[]> {
        try {
            const data: any = await this.service.get(tipo).toPromise();
            //console.log(data)

            if (data) {
                if (data.status == 200) {
                    return data.inmueble;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Información Inmueble");
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Información Inmueble");
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Información Inmueble");
        }
    }

}