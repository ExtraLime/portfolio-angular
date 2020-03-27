import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {ProjectsApiService} from './projects/projects-api.services';
import {Project} from './projects/project.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  ProjectListSubs: Subscription;
  ProjectList: Project[];

  constructor(private projectsApi: ProjectsApiService) {
  }

  ngOnInit() {
    this.ProjectListSubs = this.projectsApi
      .getProjects()
      .subscribe(res => {
          this.ProjectList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.ProjectListSubs.unsubscribe();
  }
}
