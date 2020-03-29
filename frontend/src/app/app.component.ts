import {Component, OnInit} from '@angular/core';
import * as Auth0 from 'auth0-web';

@Component({
  selector: 'app-root',
  template: `
  <mat-toolbar color="primary" class="mat-elevation-z10">
  <button mat-button>Projects</button>
  <button mat-button>About</button>

  <!-- This fills the remaining space of the current row -->
  <span class="fill-remaining-space"></span>

  <button mat-button (click)="signIn()" *ngIf="!authenticated">Sign In</button>
  <button mat-button (click)="signOut()" *ngIf="authenticated">Sign Out</button>
</mat-toolbar>
<div style="text-align:center">
      <h1>Projects</h1>
    </div>
    <h2>Here are the projects created so far: </h2>

<router-outlet></router-outlet>
  `,
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  authenticated = false;

  signIn = Auth0.signIn;
  signOut = Auth0.signOut;

  ngOnInit() {
    const self = this;
    Auth0.subscribe((authenticated) => (self.authenticated = authenticated));
  }
}