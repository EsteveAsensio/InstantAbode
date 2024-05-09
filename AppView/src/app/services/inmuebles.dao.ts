
import { Injectable } from '@angular/core';

import { BaseService } from './base.service';
import { SwalAnimation } from '../utils/SwalAnimation';
import { AuthService } from './auth-service';
import { ErrorHandlerService } from './errorHandler.service';
import { Inmueble } from '../models/inmueble.modelo';


@Injectable({
    providedIn: 'root',
})
export class InmuebleDAO {

    constructor(
        private service: BaseService,
        private errorHandler: ErrorHandlerService,
        private authService: AuthService,
    ) { }

    async getProvincias(tipo: string): Promise<void | any[]> {
        try {
            const data: any = await this.service.get(tipo).toPromise();
            if (data && data.provincias) {
                return data.provincias;
            } else {
                ///console.log(data)
                this.errorHandler.handleHttpError(data);
                return [];
            }
        } catch (error: any) {
            ///console.log(error)
            this.errorHandler.handleHttpError(error);
            return [];
        }
    }

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
                    console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Obtener Inmuebles");
                    return [];
                }
            } else {
                this.errorHandler.handleHttpError(data, false, "Obtener Inmuebles");
                return [];
            }
        } catch (error: any) {
            this.errorHandler.handleHttpError(error, false, "Obtener Inmuebles");
            return [];
        }
    }

    async realizarAlquiler(tipo: string, inmueble: Inmueble, cliente_id: number) {
        try {
            const alquilerData = {
                "cliente": cliente_id,
                "inmueble": inmueble.id,
                "fechaInicio": inmueble.fechaInicio,
                "fechaFinal": inmueble.fechaFinal
            };
            console.log(alquilerData);
            const data: any = await this.service.post(tipo, alquilerData).toPromise();

            if (data.result) {
                if (data.result.status == 200) {
                    return data.result.message;
                } else {
                    console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Obtener Inmuebles");
                    return [];
                }
            } else {
                this.errorHandler.handleHttpError(data, false, "Obtener Inmuebles");
                return [];
            }
        } catch (error: any) {
            this.errorHandler.handleHttpError(error, false, "Obtener Inmuebles");
            return [];
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
                    return [];
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Obtener Alquileres");
                return [];
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Obtener Alquileres");
            return [];
        }
    }

    async obtenerInfoInmueble(tipo: string): Promise<void | any> {
        try {
            const data: any = await this.service.get(tipo).toPromise();
            //console.log(data)

            if (data) {
                if (data.status == 200) {
                    return data.inmueble;
                } else {
                    ////console.log(data)
                    this.errorHandler.handleHttpError(data, false, "Información Inmueble");
                    return null
                }
            } else {
                ////console.log(data)
                this.errorHandler.handleHttpError(data, false, "Información Inmueble");
                return null
            }
        } catch (error: any) {
            ////console.log(error)
            this.errorHandler.handleHttpError(error, false, "Información Inmueble");
            return null
        }
    }

}