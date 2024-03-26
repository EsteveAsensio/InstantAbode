import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { PrincipalComponent } from './pages/principal/principal.component';

export const routes: Routes = [
    { component: LoginComponent, path: 'login' },
    { component: LoginComponent, path: ''},
    { component: PrincipalComponent, path: 'principal'},
    { component: LoginComponent, path: '**' }
];
