import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class SetupService {

    url = 'http://' + window.location.hostname + ':5000/';

    constructor(private http: HttpClient) {
    }

    getInfraGen() {
        return this.http.get(this.url + "infra_gen");
    }

    getInfraGenInput() {
        return this.http.get(this.url + "infra_gen_input");
    }

    getInfraGenOutput() {
        return this.http.get(this.url + "infra_gen_output");
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

    getPartitionOutput() {
        return this.http.get(this.url + "partition_output");
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

    getDeploymentInput() {
        return this.http.get(this.url + "deployment_input");
    }

    getDeploymentOutput() {
        return this.http.get(this.url + "deployment_output");
    }

    getSanityNetwork() {
        return this.http.get(this.url + "sanity_network");
    }

    getSanityCPU() {
        return this.http.get(this.url + "sanity_cpu");
    }

    getSanityPubSub() {
        return this.http.get(this.url + "pub_sub");
    }
}
