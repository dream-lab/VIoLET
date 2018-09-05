import { Component, OnInit } from '@angular/core';
import {SetupDataService} from "../setup-data.service";

@Component({
  selector: 'app-setup-partition',
  templateUrl: './setup-partition.component.html',
  styleUrls: ['./setup-partition.component.scss']
})
export class SetupPartitionComponent implements OnInit {

  constructor(public sdService: SetupDataService) { }

  ngOnInit() {
  }

}
