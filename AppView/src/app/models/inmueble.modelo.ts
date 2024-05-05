import { Alquiler } from "./alquiler.modelo";
import { Propietario } from "./propietario.modelo";
import { ValoracionInmueble } from "./valoracionInmueble.modelo";

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
      public precio: number,
      public precioAlquiler: number,
      public state: string,
      public imagenPrincipal: string,
      public imagenes : string[],
      public propietario: Propietario,
      public alquileres: Alquiler[],
      public valoraciones: ValoracionInmueble[]
    ) { }
  }
  