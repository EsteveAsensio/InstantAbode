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
            console.log(data)

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

}