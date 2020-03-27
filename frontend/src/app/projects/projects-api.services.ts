import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs-compat/Observable';
import 'rxjs/add/operator/catch';
import {API_URL} from '../env';
import {Project} from './project.model';

@Injectable()

export class ProjectsApiService {
    constructor(private http: HttpClient) {
    }

    private static _handleError(err: HttpErrorResponse | any) {
        return Observable.throw(err.message || 'Error: Unable to complete request.');
    }

    //GET list of public, future events
    getProjects(): Observable<any> {
        return this.http
        .get(`${API_URL}/projects`)
        .catch(ProjectsApiService._handleError);
    }
}