import {Component, OnInit} from '@angular/core';
import {SetupService} from "./setup.service";

@Component({
    selector: 'app-setup',
    templateUrl: './setup.component.html',
    styleUrls: ['./setup.component.scss']
})
export class SetupComponent implements OnInit {

    generateInfraStatus = '';
    generateMetisInputStatus = '';
    generatePartitionStatus = '';
    checkMetisStatus = '';
    startDockerStatus = '';
    deleteInfraStatus = '';
    infraSetupStatus = '';
    sensorGenStatus = '';
    vm: number;

    constructor(public setupService: SetupService) {
    }

    ngOnInit() {
    }

    generateInfra() {
        this.generateInfraStatus = "running";
        this.setupService.getInfraGen().subscribe(res => this.generateInfraStatus = "success",
            error => this.generateInfraStatus = "failure");
    }

    generateMetisInput() {
        this.generateMetisInputStatus = "running";
        this.setupService.getMetisInputGen().subscribe(res => this.generateMetisInputStatus = "success",
            error => this.generateMetisInputStatus = "failure");
    }

    generatePartition() {
        this.generatePartitionStatus = "running";
        console.log(this.vm);
        this.setupService.postPartitionGen(this.vm).subscribe(res => this.generatePartitionStatus = "success",
            error => this.generatePartitionStatus = "failure");
    }

    checkMetis() {
        this.checkMetisStatus = "running";
        console.log(this.vm);
        this.setupService.postCheckMetis(this.vm).subscribe(res => this.checkMetisStatus = "success",
            error => this.checkMetisStatus = "failure");
    }

    startDocker() {
        this.startDockerStatus = "running";
        this.setupService.getStartDocker().subscribe(res => this.startDockerStatus = "success",
            error => this.startDockerStatus = "failure");
    }

    deleteInfra() {
        this.deleteInfraStatus = "running";
        this.setupService.getDeleteInfra().subscribe(res => this.deleteInfraStatus = "success",
            error => this.deleteInfraStatus = "failure");
    }

    infraSetup() {
        this.infraSetupStatus = "running";
        this.setupService.getInfraSetup().subscribe(res => this.infraSetupStatus = "success",
            error => this.infraSetupStatus = "failure");
    }

    sensorGen() {
        this.sensorGenStatus = "running";
        this.setupService.getSensorGen().subscribe(res => this.sensorGenStatus = "success",
            error => this.sensorGenStatus = "failure");
    }

}
