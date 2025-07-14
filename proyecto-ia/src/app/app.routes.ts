import { Routes } from '@angular/router';
import { ImageComponent } from './image/image.component';


import { DashboardComponent } from './dashboard/dashboard.component';
import { HistorialComponent } from './historial/historial.component';

export const routes: Routes = [
    {
        path:'', component:DashboardComponent
    },
    {
        path: 'image',component: ImageComponent
    },{
        path:'historial', component:HistorialComponent
    }
];
