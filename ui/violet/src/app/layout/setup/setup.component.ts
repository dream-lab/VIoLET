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

    sanitySelection = 'N/W';
    sanityStatus = '';
    sanityNetworkStatus = '';
    sanityCPUStatus = '';
    sanityPubSubStatus = '';

    options: any = {maxLines: 1000, printMargin: false};

    vm = 3;

    currentView = 'infra';

    constructor(public setupService: SetupService,
                public setupDataService: SetupDataService) {
    }

    ngOnInit() {
        this.setupDataService.getInfraInput()
    }

    // Infra Gen

    generateInfra() {
        this.generateInfraStatus = "running";
        this.setupDataService.consoleOutput['infra'] = '';
        this.currentView = 'infra';
        this.setupService.getInfraGen().subscribe(res => {
                this.generateInfraStatus = "success";
                this.setupDataService.consoleOutput['infra'] = res['message'];
                this.setupDataService.getInfraOutput();
                this.setupDataService.getPartitionInput();
            },
            error => {
                this.generateInfraStatus = "failure";
                this.setupDataService.consoleOutput['infra'] = error.error['message'];
            }
        );
    }

    // Partition

    generateMetisInput() {
        this.generateMetisInputStatus = "running";
        this.partitionStatus = "running";
        this.currentView = 'partition';
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
                this.setupDataService.consoleOutput['partition'] += error.error['message'];
            }
        );
    }

    generatePartition() {
        this.generatePartitionStatus = "running";
        this.setupDataService.consoleOutput['partition'] += '\n2. Generating Partition...\n************************\n';
        this.setupService.postPartitionGen(this.vm).subscribe(res => {
                this.generatePartitionStatus = "success";
                this.setupDataService.consoleOutput['partition'] += res['message']
                this.checkMetis();
            },
            error => {
                this.generatePartitionStatus = "failure";
                this.partitionStatus = "failure";
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
                this.setupDataService.consoleOutput['partition'] += res['message'];
                this.setupDataService.getPartitionOutput();
            },
            error => {
                this.checkMetisStatus = "failure";
                this.partitionStatus = "failure";
                this.setupDataService.consoleOutput['partition'] += error.error['message'];
            });
    }

    // Deployment

    // getDeploymentInput() {
    //     this.setupService.getDeploymentInput().subscribe(res =>{
    //         this.inputFile = res['data'];
    //         this.input_file_name = ' - ' + res['name'];
    //     });
    // }
    //
    // getDeploymentOutput() {
    //     this.setupService.getDeploymentOutput().subscribe(res =>{
    //         this.outputFile = res['data'];
    //         this.output_file_name = ' - ' + res['name'];
    //     });
    // }
    //
    // startDocker() {
    //     this.startDockerStatus = "running";
    //     this.deploymentStatus = "running";
    //     this.getDeploymentInput();
    //     this.outputFile = '';
    //     this.output_file_name = '';
    //     this.consoleOutput = '1. Starting Docker... \n';
    //     this.setupService.getStartDocker().subscribe(res => {
    //             this.startDockerStatus = "success";
    //             this.consoleOutput += res['message'];
    //             this.deleteInfra();
    //         },
    //         error => {
    //             this.startDockerStatus = "failure";
    //             this.deploymentStatus = "failure";
    //             this.consoleOutput += error.error['message'];
    //         });
    // }
    //
    // deleteInfra() {
    //     this.deleteInfraStatus = "running";
    //     this.consoleOutput += '2. Deleting Infrastructure... \n';
    //     this.setupService.getDeleteInfra().subscribe(res =>{
    //             this.deleteInfraStatus = "success";
    //             this.consoleOutput += res['message'];
    //             this.infraSetup();
    //     },
    //         error =>  {
    //         this.deleteInfraStatus = "failure";
    //         this.deploymentStatus = "failure";
    //         this.consoleOutput += error.error['message'];
    //         });
    // }
    //
    // infraSetup() {
    //     this.infraSetupStatus = "running";
    //     this.consoleOutput += '3. Running Infrastructure setup... \n';
    //     this.setupService.getInfraSetup().subscribe(res => {
    //             this.infraSetupStatus = "success";
    //             this.consoleOutput += res['message'];
    //             this.sensorGen();
    //         },
    //         error => {
    //             this.infraSetupStatus = "failure";
    //             this.deploymentStatus = "failure";
    //             this.consoleOutput += error.error['message'];
    //         });
    // }
    //
    // sensorGen() {
    //     this.sensorGenStatus = "running";
    //     this.consoleOutput += '4. Running Sensor Gen... \n';
    //     this.setupService.getSensorGen().subscribe(res => {
    //             this.sensorGenStatus = "success";
    //             this.deploymentStatus = "success";
    //             this.consoleOutput += res['message'];
    //             this.getDeploymentOutput();
    //         },
    //         error => {
    //             this.sensorGenStatus = "failure";
    //             this.deploymentStatus = "failure";
    //             this.consoleOutput += error.error['message'];
    //         });
    // }

    // Sanity

    // getSanityInput() {
    //     this.setupService.getDeploymentOutput().subscribe(res =>{
    //         this.inputFile = res['data'];
    //         this.input_file_name = ' - ' + res['name'];
    //     });
    // }
    //
    // sanityNetwork() {
    //     this.sanityStatus = "running";
    //     this.sanityNetworkStatus = "running";
    //     this.consoleOutput = 'Running N/W sanity check... \n';
    //     this.getSanityInput();
    //     this.outputFile = '';
    //     this.output_file_name = '';
    //     this.setupService.getSanityNetwork().subscribe(res => {
    //             this.sanityNetworkStatus = "success";
    //             this.sanityStatus = "success";
    //             this.consoleOutput += res['message'];
    //         },
    //         error => {
    //             this.sanityNetworkStatus = "failure";
    //             this.sanityStatus = "failure";
    //             this.consoleOutput += "\n Failed";
    //         });
    // }
    //
    // sanityCPU() {
    //     this.sanityStatus = "running";
    //     this.sanityCPUStatus = "running";
    //     this.consoleOutput = 'Running CPU sanity check... \n';
    //     this.getSanityInput();
    //     this.outputFile = '';
    //     this.output_file_name = '';
    //     this.setupService.getSanityCPU().subscribe(res => {
    //             this.sanityCPUStatus = "success";
    //             this.sanityStatus = "success";
    //             this.consoleOutput += res['message'];
    //         },
    //         error => {
    //             this.sanityCPUStatus = "failure";
    //             this.sanityStatus = "failure";
    //             this.consoleOutput += "\n Failed";
    //         });
    // }
    //
    // sanityPubSub() {
    //     this.sanityStatus = "running";
    //     this.sanityPubSubStatus = "running";
    //     this.consoleOutput = 'Running Pub/Sub sanity check... \n';
    //     this.getSanityInput();
    //     this.outputFile = '';
    //     this.output_file_name = '';
    //     this.setupService.getSanityPubSub().subscribe(res => {
    //             this.sanityPubSubStatus = "success";
    //             this.sanityStatus = "success";
    //             this.consoleOutput += res['message'];
    //         },
    //         error => {
    //             this.sanityPubSubStatus = "failure";
    //             this.sanityStatus = "failure";
    //             this.consoleOutput += "\n Failed";
    //         });
    // }
    //
    // sanityRun() {
    //     if (this.sanitySelection === 'N/W') {
    //         this.sanityNetwork();
    //     }
    //     else if (this.sanitySelection === 'CPU') {
    //         this.sanityCPU();
    //     }
    //     else if (this.sanitySelection === 'App') {
    //         this.sanityPubSub();
    //     }
    // }

}
