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

    postPartitionGen(vm: number) {
        let formData: FormData = new FormData();
        formData.append('vm', vm.toString());
        return this.http.post(this.url + "partition_gen", formData);
    }

    postCheckMetis(vm: number) {
        let formData: FormData = new FormData();
        formData.append('vm', vm.toString());
        return this.http.post(this.url + "metis_check", formData);
    }

    getStartDocker() {
        return this.http.get(this.url + "start_docker");
    }

    getDeleteInfra() {
        return this.http.get(this.url + "delete_infra");
    }

    getInfraSetup() {
        return this.http.get(this.url + "infra_setup");
    }

    getSensorGen() {
        return this.http.get(this.url + "sensor_gen");
    }
}
