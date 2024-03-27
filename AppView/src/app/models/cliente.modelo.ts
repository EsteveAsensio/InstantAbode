import { Alquiler } from "./alquiler.modelo";
import { ValoracionCliente } from "./valoracionCliente.modelo";


export class Cliente {
  constructor(
    public id: number,
    public dni: string,
    public nombreCliente: string,
    public apellidos: string,
    public telefono: Date,
    public name: string,
    public correo: string,
    public contrasenya: string,
    public imagen: string,
    public valoraciones: ValoracionCliente[],
    public alquileres: Alquiler[]

  ) { }
}
