import { Routes } from '@angular/router';
import { ImageComponent } from './image/image.component';

import { HomeComponent } from './home/home.component';

export const routes: Routes = [
    {
        path:'', component:HomeComponent
    },
    {
        path: 'image',component: ImageComponent
    }
];
