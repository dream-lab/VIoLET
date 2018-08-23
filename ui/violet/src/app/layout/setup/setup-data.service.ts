import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class SetupDataService {

    url = 'http://' + window.location.hostname + ':5000/';

    files = {};
    images = {};

    inputFileDD = {};
    outputFileDD = {};

    consoleOutput = {};

    summaryInfraInput = {};
    summaryInfraOutput = {};
    inputInfraFile = '';
    outputInfraFile = '';
    generateInfraStatus = '';

    summaryPartitionInput = {};
    summaryPartitionOutput = {};
    inputPartitionFile = '';
    outputPartitionFile = '';
    partitionStatus = '';

    inputDepFile = '';
    outputDepFile = '';
    deploymentStatus = '';

    inputSanFile = '';
    outputSanFile = '';
    sanityStatus = '';

    constructor(private http: HttpClient) {
    }


    // Infra

    getSummaryInfraInput() {
        const temp = JSON.parse(this.files['infra_gen.json']);
        const temp1 = JSON.parse(this.files['device_types.json']);
        this.summaryInfraInput['pvt_networks'] = Object.keys(temp.private_networks).length;
        this.summaryInfraInput['pub_networks'] = Object.keys(temp.public_networks).length;
        this.summaryInfraInput['pvt_bandwidth'] = temp.network.private_networks.bandwidth_mbps.join(', ');
        this.summaryInfraInput['pub_bandwidth'] = temp.network.public_networks.bandwidth_mbps.join(', ');
        this.summaryInfraInput['pvt_latency'] = temp.network.private_networks.latency_ms.join(', ');
        this.summaryInfraInput['pub_latency'] = temp.network.public_networks.latency_ms.join(', ');
        this.summaryInfraInput['pvt_dev_cnt'] = 0;
        this.summaryInfraInput['pvt_dev'] = {};
        this.summaryInfraInput['pub_dev'] = {};
        this.summaryInfraInput['dev_cnt'] = 1;
        for (const i in temp1) {
            this.summaryInfraInput['pvt_dev'][i] = 0;
            this.summaryInfraInput['pub_dev'][i] = 0;
            this.summaryInfraInput['dev_cnt'] += 1;
        }
        for (const i in temp['private_networks']) {
            this.summaryInfraInput['pvt_dev_cnt'] += +temp['private_networks'][i]['number_devices'] + 1;
            this.summaryInfraInput['pvt_dev'][temp['private_networks'][i]['device_type']] += +temp['private_networks'][i]['number_devices'] + 1;
        }
        this.summaryInfraInput['pub_dev_cnt'] = 0;
        for (const i in temp['public_networks']) {
            for (const j of temp['public_networks'][i]) {
                this.summaryInfraInput['pub_dev_cnt'] += +j['number_devices'];
                this.summaryInfraInput['pub_dev'][j['device_type']] += +j['number_devices'];
            }
        }

    }

    getSummaryInfraOutput() {
        const temp = JSON.parse(this.files['infra_config.json']);
        const temp1 = JSON.parse(this.files['infra_gen.json']);
        const temp2 = JSON.parse(this.files['device_types.json']);
        this.summaryInfraOutput['pvt'] = temp['private_networks'];
        this.summaryInfraOutput['pub'] = temp['public_networks'];
        this.summaryInfraOutput['pvt_dev'] = {};
        this.summaryInfraOutput['pub_dev'] = {};
        for (const i in temp1['private_networks']) {
            this.summaryInfraOutput['pvt_dev'][i] = {};
            for (const j in temp2) {
                if (j === temp1['private_networks'][i]['device_type'])
                    this.summaryInfraOutput['pvt_dev'][i][j] = +temp1['private_networks'][i]['number_devices'] + 1;
                else
                    this.summaryInfraOutput['pvt_dev'][i][j] = 0;
            }
        }
        for (const i in temp1['public_networks']) {
            this.summaryInfraOutput['pub_dev'][i] = {};
            for(const k in temp2){
                this.summaryInfraOutput['pub_dev'][i][k] = 0;
            }
            for (const j of temp1['public_networks'][i]) {
                        this.summaryInfraOutput['pub_dev'][i][j['device_type']] = +j['number_devices'];
            }
        }
        console.log(this.summaryInfraOutput['pub_dev']);


    }

    getInfraInput() {
        this.http.get(this.url + "infra_gen_input").subscribe(res => {
            this.files['infra_gen.json'] = res['infra_gen.json'];
            this.files['device_types.json'] = res['device_types.json'];
            this.inputFileDD['infra'] = ['infra_gen.json'];
            this.inputInfraFile = this.inputFileDD['infra'][0];
            this.getSummaryInfraInput();
        });
    }

    getInfraOutput() {
        this.http.get(this.url + "infra_gen_output").subscribe(res => {
            this.files['infra_config.json'] = res['data'];
            this.outputFileDD['infra'] = ['infra_config.json'];
            this.outputInfraFile = this.outputFileDD['infra'][0];
            this.getSummaryInfraOutput();
        });
    }

    // Partition

    getSummaryPartitionInput() {
        this.summaryPartitionInput['vmc'] = JSON.parse(this.files['vm_config.json']);
        this.summaryPartitionInput['vmt'] = JSON.parse(this.files['vm_types.json']);
        this.summaryPartitionInput['dvt'] = JSON.parse(this.files['device_types.json']);
        this.summaryPartitionInput['vm_count'] = Object.keys(this.summaryPartitionInput['vmc']['container_VM']).length;
    }

    getSummaryPartitionOutput() {
        const temp = JSON.parse(this.files['metis_partitions.json']);
        var i = 0;
        this.summaryPartitionOutput['cnt'] = {};

        Object.entries(this.summaryPartitionInput['vmc']['container_VM']).forEach(
            ([key, value]) => {
                this.summaryPartitionOutput['cnt'][i.toString()] = {'name': key, 'cnt': 0};
                i++;
            }
        );

        for (const j in temp) {
            this.summaryPartitionOutput['cnt'][temp[j]]['cnt']++;
        }
    }

    getPartitionPlots() {
        this.http.get(this.url + "partition_plot_coremark", {responseType: 'blob'}).subscribe(res => {
            this.createImageFromBlob(res, 'partition_coremark');
            this.http.get(this.url + "partition_plot_disk", {responseType: 'blob'}).subscribe(res => {
                this.createImageFromBlob(res, 'partition_disk');
                this.http.get(this.url + "partition_plot_memory", {responseType: 'blob'}).subscribe(res => {
                    this.createImageFromBlob(res, 'partition_memory');
                });
            });
        });

    }

    getPartitionInput() {
        this.http.get(this.url + "partition_input").subscribe(res => {
            this.files['vm_config.json'] = res['vm_config.json'];
            this.files['vm_types.json'] = res['vm_types.json'];
            this.inputFileDD['partition'] = ['vm_types.json', 'vm_config.json', 'device_types.json'];
            this.inputPartitionFile = this.inputFileDD['partition'][0];
            this.getSummaryPartitionInput();
        });
    }

    getPartitionOutput() {
        this.http.get(this.url + "partition_output").subscribe(res => {
            this.files['metis_partitions.json'] = res['metis_partitions.json'];
            this.outputFileDD['partition'] = ['metis_partitions.json'];
            this.outputPartitionFile = this.outputFileDD['partition'][0];
            this.getSummaryPartitionOutput();
        });
    }

    // Deployment

    getDeploymentInput() {
        this.http.get(this.url + "deployment_input").subscribe(res => {
            this.files['deployment.json'] = res['deployment.json'];
            this.files['sensor_types.json'] = res['sensor_types.json'];
            this.inputFileDD['deployment'] = ['infra_config.json', 'vm_types.json', 'device_types.json', 'vm_config.json',
                'metis_partitions.json', 'deployment.json', 'sensor_types.json'];
            this.inputDepFile = this.inputFileDD['deployment'][0];
        });
    }

    getDeploymentOutput() {
        this.http.get(this.url + "deployment_output").subscribe(res => {
            this.files['deployment_output.json'] = res['deployment_output.json'];
            this.outputFileDD['deployment'] = ['deployment_output.json'];
            this.outputDepFile = this.outputFileDD['deployment'][0];
        });
    }

    getDeploymentPlots() {
        this.http.get(this.url + "deployment_plot", {responseType: 'blob'}).subscribe(res => {
            this.createImageFromBlob(res, 'deployment_network');
        });

    }

    createImageFromBlob(image: Blob, name: string) {
        let reader = new FileReader();
        reader.addEventListener("load", () => {
            this.images[name] = reader.result;
        }, false);

        if (image) {
            reader.readAsDataURL(image);
        }
    }

    // Sanity

    getSanityInput() {
        this.inputFileDD['sanity'] = ['infra_config.json', 'vm_config.json', 'metis_partitions.json', 'deployment.json',
            'sensor_types.json'];
        this.inputSanFile = this.inputFileDD['sanity'][0];
    }

}
