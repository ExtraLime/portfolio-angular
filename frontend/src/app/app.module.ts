import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';

import { AppComponent, } from './app.component';
import {  ProjectsApiService } from './projects/projects-api.services';

import {ProjectFormComponent} from './projects/project-form.component';
import {RouterModule, Routes} from '@angular/router';
import {ProjectsComponent} from './projects/projects.component';
import { CallbackComponent } from './projects/callback.component';
import * as Auth0 from 'auth0-web'

const appRoutes: Routes = [
  { path: 'new-project', component: ProjectFormComponent },
  { path: '', component: ProjectsComponent },
  { path: 'callback', component: CallbackComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    ProjectFormComponent,
    ProjectsComponent,
    CallbackComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(
      appRoutes,
    ),
  ],
  providers: [ProjectsApiService],
  bootstrap: [AppComponent]
})
export class AppModule { 
  constructor() {
    Auth0.configure({
      domain:'limepdx.auth0.com',
      audience: 'https://limepdx.projects',
      clientID: 'oSfpDZQGaJ3ZrtOUJgZeoxu8F2iywRQu',
      redirectUri : 'http://localhost:4200/callback',
      scope: 'openid profile manage:projects'
    });
  }
 }
