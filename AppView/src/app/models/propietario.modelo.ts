import { Inmueble } from "./inmueble.modelo";
import { ValoracionCliente } from "./valoracionCliente.modelo";


export class Propietario {
    constructor(
      public id: number,
      public dni: string,
      public nombreCliente: string,
      public apellidos: string,
      public telefono: Date,
      public name: string,
      public contrasenya: string,
      public imagen: string,
      public valoracionesClientes: ValoracionCliente[],
      public inmuebles: Inmueble[]
    ) { }
  }
  