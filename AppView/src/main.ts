import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { OdooInterceptor } from './app/interceptor/odoo.interceptor';

bootstrapApplication(AppComponent, {
  ...appConfig,
  providers: [
    ...(appConfig.providers || []),
    { provide: HTTP_INTERCEPTORS, useClass: OdooInterceptor, multi: true }
  ]
}).catch((err) => console.error(err));
