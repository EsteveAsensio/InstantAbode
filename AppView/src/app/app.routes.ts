import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { PrincipalComponent } from './pages/principal/principal.component';
import { RegistrarComponent } from './pages/registrar/registrar.component';
import { PerfilUsuarioComponent } from './pages/perfil-usuario/perfil-usuario.component';

export const routes: Routes = [
    { component: LoginComponent, path: 'login' },
   
    { component: PrincipalComponent, path: 'principal'},
    { component: PerfilUsuarioComponent, path: 'perfil-usuario'},
    { component: RegistrarComponent, path: 'registrar' },

    //
    { component: LoginComponent, path: ''},
    { component: LoginComponent, path: '**' }
    

];
