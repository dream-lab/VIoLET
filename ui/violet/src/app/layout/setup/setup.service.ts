import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class SetupService {

    url = "http://localhost:5000/";

    constructor(private http: HttpClient) {
    }

    getInfraGen() {
        return this.http.get(this.url + "infra_gen");
    }

    getMetisInputGen() {
        return this.http.get(this.url + "metis_gen");
    }
}
