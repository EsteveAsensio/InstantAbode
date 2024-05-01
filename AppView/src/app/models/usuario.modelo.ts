import { Alquiler } from "./alquiler.modelo";
import { Inmueble } from "./inmueble.modelo";
import { ValoracionCliente } from "./valoracionCliente.modelo";
import { ValoracionInmueble } from "./valoracionInmueble.modelo";


export class Usuario {
    constructor(
      public id: number,
      public dni: string,
      public nombreCliente: string,
      public apellidos: string,
      public telefono: number,
      public name: string,
      public contrasenya: string,
      public correo: string,
      public imagen: string,
      public rol: string,
      public valoracionesClientes: ValoracionCliente[],
      public inmuebles: Inmueble[],     
      public valoraciones: ValoracionInmueble[],
      public alquileres: Alquiler[]
    ) { }
  }
  