import * as Auth0 from 'auth0-web';
import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {Project} from './project.model';
import {ProjectsApiService} from './projects-api.services';

@Component({
  selector: 'projects',
  template: `
  <h2>Projects</h2>
    <p>Choose an exam and start studying.</p>
    <div class="projects">
      <mat-card class="example-card" *ngFor="let project of projectsList" class="mat-elevation-z5">
        <mat-card-content>
          <mat-card-title>{{project.title}}</mat-card-title>
          <mat-card-subtitle>{{project.description}}</mat-card-subtitle>
          <p>
            Etiam enim purus, vehicula nec dapibus quis, egestas eu quam.
            Nullam eleifend auctor leo, vitae rhoncus mi sodales vel.
            Aenean fermentum laoreet volutpat. Integer quam orci,
            molestie non nibh suscipit, faucibus euismod sapien.
          </p>
          <button mat-raised-button color="accent">See Project</button>
        </mat-card-content>
      </mat-card>
    </div>
    <button mat-fab color="primary" *ngIf="authenticated"
            class="new-project" routerLink="/new-project">
      <i class="material-icons">note_add</i>
    </button>
  `,
  styleUrls: ['projects.component.scss'],
})
export class ProjectsComponent implements OnInit, OnDestroy {
  projectsListSubs: Subscription;
  projectsList: Project[];
  authenticated = false;

  constructor(private projectsApi: ProjectsApiService) { }

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