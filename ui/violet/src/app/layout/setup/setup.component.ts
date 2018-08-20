import {Component, OnInit} from '@angular/core';
import {SetupService} from "./setup.service";

@Component({
    selector: 'app-setup',
    templateUrl: './setup.component.html',
    styleUrls: ['./setup.component.scss']
})
export class SetupComponent implements OnInit {

    generateInfraStatus = '';

    partitionStatus = '';
    generateMetisInputStatus = '';
    generatePartitionStatus = '';
    checkMetisStatus = '';

    deploymentStatus = '';
    startDockerStatus = '';
    deleteInfraStatus = '';
    infraSetupStatus = '';
    sensorGenStatus = '';

    sanitySelection = 'N/W';
    sanityStatus = '';
    sanityNetworkStatus = '';
    sanityCPUStatus = '';
    sanityPubSubStatus = '';

    input_file = '';
    output_file = '';
    input_file_name = '';
    output_file_name = '';
    console_output = '';
    data = "A quick brown fox jumps over the lazy dog";
    options: any = {maxLines: 1000, printMargin: false};

    vm = 3;

    constructor(public setupService: SetupService) {
    }

    ngOnInit() {
    }

    getInfraInput() {
        this.setupService.getInfraGenInput().subscribe(res => {
            this.input_file = res['data'];
            this.input_file_name = ' - ' + res['name'];
        });
    }

    getInfraOutput() {
        this.setupService.getInfraGenOutput().subscribe(res => {
            this.output_file = res['data'];
            this.output_file_name = ' - ' + res['name'];
        });
    }

    generateInfra() {
        this.generateInfraStatus = "running";
        this.getInfraInput();
        this.output_file = '';
        this.console_output = '';
        this.setupService.getInfraGen().subscribe(res => {
                this.generateInfraStatus = "success";
                this.console_output = res['message'];
                this.getInfraOutput();
            },
            error => {
                this.generateInfraStatus = "failure";
                this.console_output = error.error['message'];
            }
        );
    }

    getPartitionOutput() {
        this.setupService.getPartitionOutput().subscribe(res =>{
            this.output_file = res['data'];
            this.output_file_name = ' - ' + res['name'];
        });
    }

    generateMetisInput() {
        this.generateMetisInputStatus = "running";
        this.partitionStatus = "running";
        this.input_file = this.output_file;
        this.input_file_name = this.output_file_name;
        this.output_file = '';
        this.output_file_name = '';
        this.console_output = '1. Generating Metis Input... \n';
        this.setupService.getMetisInputGen().subscribe(res => {
                this.generateMetisInputStatus = "success";
                this.console_output += res['message'];
                this.generatePartition();
            },
            error => {
                this.generateMetisInputStatus = "failure";
                this.partitionStatus = "failure";
                this.console_output += error.error['message'];
            }
        );
    }

    generatePartition() {
        this.generatePartitionStatus = "running";
        this.console_output += '\n2. Generating Partition... \n';
        this.setupService.postPartitionGen(this.vm).subscribe(res => {
                this.generatePartitionStatus = "success";
                this.console_output += res['message']
                this.checkMetis();
            },
            error => {
                this.generatePartitionStatus = "failure";
                this.partitionStatus = "failure";
                this.console_output += error.error['message'];
            }
        );
    }

    checkMetis() {
        this.checkMetisStatus = "running";
        this.console_output += '\n3. Running Metis Check \n';
        this.setupService.postCheckMetis(this.vm).subscribe(res => {
                this.checkMetisStatus = "success";
                this.partitionStatus = "success";
                this.console_output += res['message'];
                this.getPartitionOutput();
            },
            error => {
                this.checkMetisStatus = "failure";
                this.partitionStatus = "failure";
                this.console_output += error.error['message'];
            });
    }

    getDeploymentInput() {
        this.setupService.getDeploymentInput().subscribe(res =>{
            this.input_file = res['data'];
            this.input_file_name = ' - ' + res['name'];
        });
    }

    getDeploymentOutput() {
        this.setupService.getDeploymentOutput().subscribe(res =>{
            this.output_file = res['data'];
            this.output_file_name = ' - ' + res['name'];
        });
    }

    startDocker() {
        this.startDockerStatus = "running";
        this.deploymentStatus = "running";
        this.getDeploymentInput();
        this.output_file = '';
        this.output_file_name = '';
        this.console_output = '1. Starting Docker... \n';
        this.setupService.getStartDocker().subscribe(res => {
                this.startDockerStatus = "success";
                this.console_output += res['message'];
                this.deleteInfra();
            },
            error => {
                this.startDockerStatus = "failure";
                this.deploymentStatus = "failure";
                this.console_output += error.error['message'];
            });
    }

    deleteInfra() {
        this.deleteInfraStatus = "running";
        this.console_output += '2. Deleting Infrastructure... \n';
        this.setupService.getDeleteInfra().subscribe(res =>{
                this.deleteInfraStatus = "success";
                this.console_output += res['message'];
                this.infraSetup();
        },
            error =>  {
            this.deleteInfraStatus = "failure";
            this.deploymentStatus = "failure";
            this.console_output += error.error['message'];
            });
    }

    infraSetup() {
        this.infraSetupStatus = "running";
        this.console_output += '3. Running Infrastructure setup... \n';
        this.setupService.getInfraSetup().subscribe(res => {
                this.infraSetupStatus = "success";
                this.console_output += res['message'];
                this.sensorGen();
            },
            error => {
                this.infraSetupStatus = "failure";
                this.deploymentStatus = "failure";
                this.console_output += error.error['message'];
            });
    }

    sensorGen() {
        this.sensorGenStatus = "running";
        this.console_output += '4. Running Sensor Gen... \n';
        this.setupService.getSensorGen().subscribe(res => {
                this.sensorGenStatus = "success";
                this.deploymentStatus = "success";
                this.console_output += res['message'];
                this.getDeploymentOutput();
            },
            error => {
                this.sensorGenStatus = "failure";
                this.deploymentStatus = "failure";
                this.console_output += error.error['message'];
            });
    }

    sanityNetwork() {
        this.sanityStatus = "running";
        this.sanityNetworkStatus = "running";
        this.setupService.getSanityNetwork().subscribe(res => {
                this.sanityNetworkStatus = "success";
                this.sanityStatus = "success";
            },
            error => {
                this.sanityNetworkStatus = "failure";
                this.sanityStatus = "failure";
            });
    }

    sanityCPU() {
        this.sanityStatus = "running";
        this.sanityCPUStatus = "running";
        this.setupService.getSanityCPU().subscribe(res => {
                this.sanityCPUStatus = "success";
                this.sanityStatus = "success";
            },
            error => {
                this.sanityCPUStatus = "failure";
                this.sanityStatus = "failure";
            });
    }

    sanityPubSub() {
        this.sanityStatus = "running";
        this.sanityPubSubStatus = "running";
        this.setupService.getSanityPubSub().subscribe(res => {
                this.sanityPubSubStatus = "success";
                this.sanityStatus = "success";
            },
            error => {
                this.sanityPubSubStatus = "failure";
                this.sanityStatus = "failure";
            });
    }

    sanityRun() {
        if (this.sanitySelection === 'N/W') {
            this.sanityNetwork();
        }
        else if (this.sanitySelection === 'CPU') {
            this.sanityCPU();
        }
        else if (this.sanitySelection === 'App') {
            this.sanityPubSub();
        }
    }

}
