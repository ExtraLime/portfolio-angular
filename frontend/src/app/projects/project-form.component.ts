import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ProjectsApiService} from "./projects-api.services";
import {Router} from "@angular/router";

@Component({
  selector: 'project-form',
  template: `
    <div>
      <h2>New Project</h2>
      <label for="project-title">Title</label>
      <input id="project-title" (keyup)="updateTitle($event)">
      <label for="project-description">Description</label>
      <input id="project-description" (keyup)="updateDescription($event)">
      <button (click)="saveProject()">Save Project</button>
    </div>
  `
})
export class ProjectFormComponent {
  project = {
    title: '',
    description: '',
  };

  constructor(private projectsApi: ProjectsApiService, private router: Router) { }

  updateTitle(event: any) {
    this.project.title = event.target.value;
  }

  updateDescription(event: any) {
    this.project.description = event.target.value;
  }

  saveProject() {
    this.projectsApi
      .saveProject(this.project)
      .subscribe(
        () => this.router.navigate(['/']),
        error => alert(error.message)
      );
  }
}