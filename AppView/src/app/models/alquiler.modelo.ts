import { Cliente } from "./cliente.modelo";
import { Inmueble } from "./inmueble.modelo";
import { ValoracionInmueble } from "./valoracionInmueble.modelo";


export class Alquiler {
    constructor(
      public id: number,
      public name: string,
      public fechaInicio: Date,
      public fechaFinal: Date,
      public inmueble: Inmueble,
      public cliente: Cliente,
      public valoracionInmueble: ValoracionInmueble,
      public precio: number
    ) { }
  }