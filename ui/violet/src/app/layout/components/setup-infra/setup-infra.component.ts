import { Component, OnInit } from '@angular/core';
import {SetupDataService} from "../../setup/setup-data.service";

@Component({
  selector: 'app-setup-infra',
  templateUrl: './setup-infra.component.html',
  styleUrls: ['./setup-infra.component.scss']
})
export class SetupInfraComponent implements OnInit {


  constructor(public sdService: SetupDataService) { }

  ngOnInit() {
  }

}
