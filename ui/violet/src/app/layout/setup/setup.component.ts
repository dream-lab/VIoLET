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
    console_output = '';
    data = "A quick brown fox jumps over the lazy dog";
    options: any = {maxLines: 1000, printMargin: false};

    vm = 20;

    constructor(public setupService: SetupService) {
    }

    ngOnInit() {
    }

    getInfraInput() {
        this.setupService.getInfraGenInput().subscribe(res => this.input_file = res['data']);
    }

    getInfraOutput() {
        this.setupService.getInfraGenOutput().subscribe(res => this.output_file = res['data']);
    }

    generateInfra() {
        this.generateInfraStatus = "running";
        this.getInfraInput();
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

    generateMetisInput() {
        this.generateMetisInputStatus = "running";
        this.partitionStatus = "running";
        this.setupService.getMetisInputGen().subscribe(res => {
                this.generateMetisInputStatus = "success";
                this.generatePartition();
            },
            error => {
                this.generateMetisInputStatus = "failure";
                this.partitionStatus = "failure";
            }
        );
    }

    generatePartition() {
        this.generatePartitionStatus = "running";
        console.log(this.vm);
        this.setupService.postPartitionGen(this.vm).subscribe(res => {
                this.generatePartitionStatus = "success";
                this.checkMetis();
            },
            error => {
                this.generatePartitionStatus = "failure";
                this.partitionStatus = "failure";
            }
        );
    }

    checkMetis() {
        this.checkMetisStatus = "running";
        console.log(this.vm);
        this.setupService.postCheckMetis(this.vm).subscribe(res => {
                this.checkMetisStatus = "success";
                this.partitionStatus = "Success";
            },
            error => {
                this.checkMetisStatus = "failure";
                this.partitionStatus = "failure";
            });
    }

    startDocker() {
        this.startDockerStatus = "running";
        this.deploymentStatus = "running";
        this.setupService.getStartDocker().subscribe(res => {
                this.startDockerStatus = "success";
                this.infraSetup();
            },
            error => {
                this.startDockerStatus = "failure";
                this.deploymentStatus = "failure";
            });
    }

    deleteInfra() {
        this.deleteInfraStatus = "running";
        this.setupService.getDeleteInfra().subscribe(res => this.deleteInfraStatus = "success",
            error => this.deleteInfraStatus = "failure");
    }

    infraSetup() {
        this.infraSetupStatus = "running";
        this.setupService.getInfraSetup().subscribe(res => {
                this.infraSetupStatus = "success";
                this.sensorGen();
            },
            error => {
                this.infraSetupStatus = "failure";
                this.deploymentStatus = "failure";
            });
    }

    sensorGen() {
        this.sensorGenStatus = "running";
        this.setupService.getSensorGen().subscribe(res => {
                this.sensorGenStatus = "success";
                this.deploymentStatus = "success";
            },
            error => {
                this.sensorGenStatus = "failure";
                this.deploymentStatus = "failure";
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
