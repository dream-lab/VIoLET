import { Component, OnInit } from '@angular/core';
import {SetupDataService} from "../../setup/setup-data.service";

@Component({
  selector: 'app-setup-deployment',
  templateUrl: './setup-deployment.component.html',
  styleUrls: ['./setup-deployment.component.scss']
})
export class SetupDeploymentComponent implements OnInit {

  constructor(public sdService: SetupDataService) { }

  ngOnInit() {
  }

}
