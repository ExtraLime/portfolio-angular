import * as Auth0 from 'auth0-web';
import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {Project} from './project.model';
import {ProjectsApiService} from './projects-api.services';

@Component({
  selector: 'projects',
  template: `
    <div>
      <button routerLink="/new-project">New Project</button>
      <button (click)="signIn()" *ngIf="!authenticated">Sign In</button>
      <button (click)="signOut()" *ngIf="authenticated">Sign Out</button>
      <p *ngIf="authenticated">Hello, {{getProfile().name}}</p>
      <ul>
        <li *ngFor="let project of projectsList">
          {{project.title}}
        </li>
      </ul>
    </div>
  `
})
export class ProjectsComponent implements OnInit, OnDestroy {
  projectsListSubs: Subscription;
  projectsList: Project[];
  authenticated = false;

  constructor(private projectsApi: ProjectsApiService) { }

  signIn = Auth0.signIn;
  signOut = Auth0.signOut;
  getProfile = Auth0.getProfile;

  ngOnInit() {
    this.projectsListSubs = this.projectsApi
      .getProjects()
      .subscribe(res => {
          this.projectsList = res;
        },
        console.error
      );
    const self = this;
    Auth0.subscribe((authenticated) => (self.authenticated = authenticated));
  }

  ngOnDestroy() {
    this.projectsListSubs.unsubscribe();
  }
}