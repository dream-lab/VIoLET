import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class SetupService {

    url = 'http://' + window.location.hostname + ':5000/';
    // url = 'http://' + '104.211.75.75' + ':5000/';

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

    getSanityNetwork() {
        return this.http.get(this.url + "sanity_network");
    }

    getSanityCPU1() {
        return this.http.get(this.url + "sanity_cpu_1");
    }

    getSanityCPU2() {
        return this.http.get(this.url + "sanity_cpu_2");
    }

    getSanityPubSub() {
        return this.http.get(this.url + "pub_sub");
    }
}
