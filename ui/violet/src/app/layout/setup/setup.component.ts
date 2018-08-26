import {Component, OnInit} from '@angular/core';
import {SetupService} from "./setup.service";
import {SetupDataService} from "./setup-data.service";

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

    sanitySelection = 'CPU';
    sanityStatus = '';
    sanityNetworkStatus = '';
    sanityCPUStatus = '';
    sanityPubSubStatus = '';

    options: any = {maxLines: 1000, printMargin: false};

    vm = 3;

    currentView = 'infra';

    start: any;
    start1: any;
    end: any;

    constructor(public setupService: SetupService,
                public setupDataService: SetupDataService) {
    }

    ngOnInit() {
        this.setupDataService.getInfraInput();
        // this.setupDataService.getPartitionOutput();
        // this.setupDataService.getPartitionPlots();
        // this.setupDataService.getDeploymentInput();
        // this.setupDataService.getDeploymentOutput();
        // this.setupDataService.getDeploymentPlots();
        // this.setupDataService.getSanityCPUPlots();
    }

    // Infra Gen

    generateInfra() {
        this.generateInfraStatus = "running";
        this.setupDataService.generateInfraStatus = "running";
        this.setupDataService.consoleOutput['infra'] = '';
        this.currentView = 'infra';
        this.setupService.getInfraGen().subscribe(res => {
                this.generateInfraStatus = "success";
                this.setupDataService.generateInfraStatus = "success";
                this.setupDataService.consoleOutput['infra'] = res['message'];
                this.setupDataService.getInfraOutput();
                this.setupDataService.getPartitionInput();
            },
            error => {
                this.generateInfraStatus = "failure";
                this.setupDataService.generateInfraStatus = "failure";
                this.setupDataService.consoleOutput['infra'] = error.error['message'];
            }
        );
    }

    // Partition

    generateMetisInput() {
        this.currentView = 'partition';
        if(this.partitionStatus==='running'){
            return;
        }
        this.generateMetisInputStatus = "running";
        this.partitionStatus = "running";
        this.setupDataService.partitionStatus = "running";
        this.setupDataService.getPartitionInput();
        this.setupDataService.consoleOutput['partition'] = '1. Generating Metis Input...\n*************************\n';
        this.setupService.getMetisInputGen().subscribe(res => {
                this.generateMetisInputStatus = "success";
                this.setupDataService.consoleOutput['partition'] += res['message'];
                this.generatePartition();
            },
            error => {
                this.generateMetisInputStatus = "failure";
                this.partitionStatus = "failure";
                this.setupDataService.partitionStatus = "failure";
                this.setupDataService.consoleOutput['partition'] += error.error['message'];
            }
        );
    }

    generatePartition() {
        this.generatePartitionStatus = "running";
        this.setupDataService.consoleOutput['partition'] += '\n2. Generating Partition...\n************************\n';
        this.setupService.postPartitionGen(this.vm).subscribe(res => {
                this.generatePartitionStatus = "success";
                this.setupDataService.consoleOutput['partition'] += res['message'];
                this.checkMetis();
            },
            error => {
                this.generatePartitionStatus = "failure";
                this.partitionStatus = "failure";
                this.setupDataService.partitionStatus = "failure";
                this.setupDataService.consoleOutput['partition'] += error.error['message'];
            }
        );
    }

    checkMetis() {
        this.checkMetisStatus = "running";
        this.setupDataService.consoleOutput['partition'] += '\n3. Running Metis Check\n****************************\n';
        this.setupService.postCheckMetis(this.vm).subscribe(res => {
                this.checkMetisStatus = "success";
                this.partitionStatus = "success";
                this.setupDataService.partitionStatus = "success";
                this.setupDataService.consoleOutput['partition'] += res['message'];
                this.setupDataService.getPartitionOutput();
                this.setupDataService.getPartitionPlots();
                this.setupDataService.getDeploymentInput();
            },
            error => {
                this.checkMetisStatus = "failure";
                this.partitionStatus = "failure";
                this.setupDataService.partitionStatus = "failure";
                this.setupDataService.consoleOutput['partition'] += error.error['message'];
            });
    }

    // Deployment

    startDocker() {
        this.currentView = 'deployment';
        if(this.deploymentStatus==='running'){
            return;
        }
        this.startDockerStatus = "running";
        this.deploymentStatus = "running";
        this.setupDataService.deploymentStatus = "running";
        this.setupDataService.consoleOutput['deployment'] = '1. Starting Docker... \n******************************\n';
        this.start = this.start1 = Date.now();
        this.setupService.getStartDocker().subscribe(res => {
                this.startDockerStatus = "success";
                this.setupDataService.consoleOutput['deployment'] += res['message'];
                this.end = Date.now();
                this.setupDataService.consoleOutput['deployment'] += 'Time elapsed: ' + ((this.end - this.start1) / 1000).toString() + 's \n\n';
                this.deleteInfra();
            },
            error => {
                this.startDockerStatus = "failure";
                this.deploymentStatus = "failure";
                this.setupDataService.deploymentStatus = "failure";
                this.setupDataService.consoleOutput['deployment'] += error.error['message'];
            });
    }

    deleteInfra() {
        this.deleteInfraStatus = "running";
        this.start1 = Date.now();
        this.setupDataService.consoleOutput['deployment'] += '\n 2. Deleting Old Infrastructure...\n******************************\n';
        this.setupService.getDeleteInfra().subscribe(res => {
                this.deleteInfraStatus = "success";
                this.setupDataService.consoleOutput['deployment'] += res['message'];
                this.end = Date.now();
                this.setupDataService.consoleOutput['deployment'] += '\n\nTime elapsed: ' + ((this.end - this.start1) / 1000).toString() + 's \n\n';
                this.infraSetup();
            },
            error => {
                this.deleteInfraStatus = "failure";
                this.deploymentStatus = "failure";
                this.setupDataService.deploymentStatus = "failure";
                this.setupDataService.consoleOutput['deployment'] += error.error['message'];
            });
    }

    infraSetup() {
        this.infraSetupStatus = "running";
        this.start1 = Date.now();
        this.setupDataService.consoleOutput['deployment'] += '\n3. Setting up Infrastructure...\n********************************\n';
        this.setupService.getInfraSetup().subscribe(res => {
                this.infraSetupStatus = "success";
                this.setupDataService.consoleOutput['deployment'] += res['message'];
                this.end = Date.now();
                this.setupDataService.consoleOutput['deployment'] += '\n\nTime elapsed: ' + ((this.end - this.start1) / 1000).toString() + 's \n\n';
                this.sensorGen();
            },
            error => {
                this.infraSetupStatus = "failure";
                this.deploymentStatus = "failure";
                this.setupDataService.deploymentStatus = "failure";
                this.setupDataService.consoleOutput['deployment'] += error.error['message'];
            });
    }

    sensorGen() {
        this.sensorGenStatus = "running";
        this.start1 = Date.now();
        this.setupDataService.consoleOutput['deployment'] += '\n4. Generating Sensors...\n******************************\n';
        this.setupService.getSensorGen().subscribe(res => {
                this.sensorGenStatus = "success";
                this.deploymentStatus = "success";
                this.setupDataService.deploymentStatus = "success";
                this.setupDataService.consoleOutput['deployment'] += res['message'];
                this.end = Date.now();
                this.setupDataService.consoleOutput['deployment'] += '\n\nTime elapsed: ' + ((this.end - this.start1) / 1000).toString() + 's \n\n';
                this.setupDataService.consoleOutput['deployment'] += '\n\nTotal Time elapsed: ' + ((this.end - this.start) / 1000).toString() + 's \n\n';
                this.setupDataService.getDeploymentOutput();
                this.setupDataService.getDeploymentPlots();
                this.setupDataService.getSanityInput();
            },
            error => {
                this.sensorGenStatus = "failure";
                this.deploymentStatus = "failure";
                this.setupDataService.deploymentStatus = "failure";
                this.setupDataService.consoleOutput['deployment'] += error.error['message'];
            });
    }

    // Sanity

    sanityNetwork() {
        this.sanityStatus = "running";
        this.setupDataService.sanityStatus = "running";
        this.sanityNetworkStatus = "running";
        this.setupDataService.consoleOutput['sanity'] = 'Running N/W Micro benchmark... \n*****************************\n';
        this.setupService.getSanityNetwork().subscribe(res => {
                this.sanityNetworkStatus = "success";
                this.sanityStatus = "success";
                this.setupDataService.sanityStatus = "success";
                this.setupDataService.consoleOutput['sanity'] += res['message'];
            },
            error => {
                this.sanityNetworkStatus = "failure";
                this.sanityStatus = "failure";
                this.setupDataService.sanityStatus = "failure";
                this.setupDataService.consoleOutput['sanity'] += "\n Failed";
            });
    }

    sanityCPU1() {
        this.sanityStatus = "running";
        this.setupDataService.sanityStatus = "running";
        this.sanityCPUStatus = "running";
        this.setupDataService.consoleOutput['sanity'] = '1. Starting CPU Micro benchmark... \n***************************\n\n';
        this.start = this.start1 = Date.now();
        this.setupService.getSanityCPU1().subscribe(res => {
                this.setupDataService.consoleOutput['sanity'] += res['message'];
                this.end = Date.now();
                this.setupDataService.consoleOutput['sanity'] += '\n\nTime elapsed: ' + ((this.end - this.start1) / 1000).toString() + 's \n\n';
                this.setupDataService.consoleOutput['sanity'] += '\nWaiting for 5 minutes... \n\n'
                setTimeout(() => {this.sanityCPU2();},   300000);
            },
            error => {
                this.sanityCPUStatus = "failure";
                this.sanityStatus = "failure";
                this.setupDataService.sanityStatus = "failure";
                this.setupDataService.consoleOutput['sanity'] += "\n Failed";
            });
    }

    sanityCPU2() {
        this.start1 = Date.now();
        this.setupDataService.consoleOutput['sanity'] += '2. Collecting Coremark data... \n*****************************\n\n';
        this.setupService.getSanityCPU2().subscribe(res => {
                this.sanityCPUStatus = "success";
                this.sanityStatus = "success";
                this.setupDataService.sanityStatus = "success";
                this.setupDataService.consoleOutput['sanity'] += res['message'];
                this.end = Date.now();
                this.setupDataService.consoleOutput['sanity'] += '\n\nTime elapsed: ' + ((this.end - this.start1) / 1000).toString() + 's \n\n';
                this.setupDataService.consoleOutput['sanity'] += '\n\nTotal Time elapsed: ' + ((this.end - this.start) / 1000).toString() + 's \n\n';
                this.setupDataService.getSanityCPUPlots();
            },
            error => {
                this.sanityCPUStatus = "failure";
                this.sanityStatus = "failure";
                this.setupDataService.sanityStatus = "failure";
                this.setupDataService.consoleOutput['sanity'] += "\n Failed";
            });
    }

    sanityPubSub() {
        this.sanityStatus = "running";
        this.setupDataService.sanityStatus = "running";
        this.sanityPubSubStatus = "running";
        this.setupDataService.consoleOutput['sanity'] = 'Running Pub/Sub Micro benchmark... \n*************************\n';
        this.setupService.getSanityPubSub().subscribe(res => {
                this.sanityPubSubStatus = "success";
                this.sanityStatus = "success";
                this.setupDataService.sanityStatus = "success";
                this.setupDataService.consoleOutput['sanity'] += res['message'];
            },
            error => {
                this.sanityPubSubStatus = "failure";
                this.sanityStatus = "failure";
                this.setupDataService.sanityStatus = "failure";
                this.setupDataService.consoleOutput['sanity'] += "\n Failed";
            });
    }

    sanityRun() {

        this.currentView = 'sanity';

        if(this.sanityStatus==='running') {
            return;
        }

        if (this.sanitySelection === 'N/W') {
            this.sanityNetwork();
        }
        else if (this.sanitySelection === 'CPU') {
            this.sanityCPU1();
        }
        else if (this.sanitySelection === 'App') {
            this.sanityPubSub();
        }
    }

}
