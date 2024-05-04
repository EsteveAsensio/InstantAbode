import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { PrincipalComponent } from './pages/principal/principal.component';
import { RegistrarComponent } from './pages/registrar/registrar.component';
import { PerfilUsuarioComponent } from './pages/perfil-usuario/perfil-usuario.component';
import { InmueblesAlquiladosComponent } from './pages/inmuebles-alquilados/inmuebles-alquilados.component';
import { ValoracionesInmueblesComponent } from './pages/valoraciones-inmuebles/valoraciones-inmuebles.component';
import { InformacionInmuebleComponent } from './pages/informacion-inmueble/informacion-inmueble.component';

export const routes: Routes = [
    { component: LoginComponent, path: 'login' },
   
    { component: PrincipalComponent, path: 'principal'},
    { component: InformacionInmuebleComponent, path: 'inmueble/:id'},
    { component: PerfilUsuarioComponent, path: 'perfil-usuario'},
    { component: InmueblesAlquiladosComponent, path: 'inmuebles-alquilados'},
    { component: ValoracionesInmueblesComponent, path: 'valoraciones-inmuebles'},
    { component: RegistrarComponent, path: 'registrar' },

    //
    { component: LoginComponent, path: ''},
    { component: LoginComponent, path: '**' }
    

];
