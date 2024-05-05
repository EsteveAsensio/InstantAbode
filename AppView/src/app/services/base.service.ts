import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable, catchError, map, throwError } from 'rxjs';
import { URL_BACKEND } from './constantesHTTP';


@Injectable({
  providedIn: 'root',
})
export class BaseService {
  constructor(private http: HttpClient) { }

  public get<T>(path: string) {
    return this.http.get<T>(`${URL_BACKEND}${path}`);
  }
  public getUno<T>(path: string) {
    return this.http.get<T>(`${URL_BACKEND}${path}`);
  }
  public getFiltrados<T>(path: string, filtro: any) {
    return this.http.post<T>(`${URL_BACKEND}${path}`,filtro);
  }
  public post<T>(path: string, data: any): Observable<T> {
    return this.http.post<T>(`${URL_BACKEND}${path}`, data);
  }
  public put<T>(path: string, data: any): Observable<T> {
    return this.http.put<T>(`${URL_BACKEND}${path}`, data);
  }
  public delete<T>(path: string, data: any): any {
    return this.http.delete<T>(`${URL_BACKEND}${path}`, data);
  }
  
  public deleteUno<T>(path: string): any {
    return this.http.delete<T>(`${URL_BACKEND}${path}`);
  }


  public cambioDeContrasena<T>(pathObject: string, data: any) {
    const url = `${URL_BACKEND}${pathObject}`;
    return this.http.post<T>(url, data, {
    });
  }
}
