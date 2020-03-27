import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';

import { AppComponent, } from './app.component';
import {  ProjectsApiService } from './projects/projects-api.services';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
  ],
  providers: [ProjectsApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
