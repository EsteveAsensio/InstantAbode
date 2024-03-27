import { Cliente } from "./cliente.modelo";
import { Propietario } from "./propietario.modelo";


export class ValoracionCliente {
    constructor(
      public id: number,
      public name: string,
      public comentario: string,
      public puntuacion: number,
      public fecha: Date,
      public propietario: Propietario,
      public cliente: Cliente
    ) { }
  }