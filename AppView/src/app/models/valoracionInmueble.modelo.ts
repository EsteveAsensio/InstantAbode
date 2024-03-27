import { Alquiler } from "./alquiler.modelo";
import { Cliente } from "./cliente.modelo";
import { Inmueble } from "./inmueble.modelo";


export class ValoracionInmueble {
    constructor(
      public id: number,
      public name: string,
      public comentario: string,
      public puntuacion: number,
      public fecha: Date,
      public inmueble: Inmueble,
      public cliente: Cliente,
      public alquiler: Alquiler
    ) { }
  }