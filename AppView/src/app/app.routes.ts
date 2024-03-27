import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { PrincipalComponent } from './pages/principal/principal.component';
import { RegistrarComponent } from './pages/registrar/registrar.component';

export const routes: Routes = [
    { component: LoginComponent, path: 'login' },
   
    { component: PrincipalComponent, path: 'principal'},
    { component: RegistrarComponent, path: 'registrar' },

    //
    { component: LoginComponent, path: ''},
    { component: LoginComponent, path: '**' }
    

];
