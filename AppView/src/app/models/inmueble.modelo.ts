import { Alquiler } from "./alquiler.modelo";
import { Propietario } from "./propietario.modelo";

export class Inmueble {
    constructor(
      public id: number,
      public name: string,
      public provincia: string,
      public localizacion: string,
      public habitaciones: number,
      public banyos: number,
      public metrosCuadrados: number,
      public descripcion: string,
      public adicionales: string,
      public state: string,
      public propietario: Propietario,
      public alquileres: Alquiler[]
    ) { }
  }
  