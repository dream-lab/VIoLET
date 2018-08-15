import { Component, OnInit } from '@angular/core';
import {SetupService} from "./setup.service";

@Component({
  selector: 'app-setup',
  templateUrl: './setup.component.html',
  styleUrls: ['./setup.component.scss']
})
export class SetupComponent implements OnInit {

  generateInfraStatus = '';
  generateMetisInputStatus = '';

  constructor(public setupService: SetupService) { }

  ngOnInit() {
  }

  generateInfra(){
      this.generateInfraStatus = "running";
      this.setupService.getInfraGen().subscribe(res => this.generateInfraStatus = "success",
          error => this.generateInfraStatus = "failure");
  }

    generateMetisInput(){
        this.generateMetisInputStatus = "running";
        this.setupService.getMetisInputGen().subscribe(res => this.generateMetisInputStatus = "success",
            error => this.generateMetisInputStatus = "failure");
    }

}
