import { Component, OnInit } from '@angular/core';
import {SetupDataService} from "../../setup/setup-data.service";

@Component({
  selector: 'app-setup-sanity',
  templateUrl: './setup-sanity.component.html',
  styleUrls: ['./setup-sanity.component.scss']
})
export class SetupSanityComponent implements OnInit {

  constructor(public sdService: SetupDataService) { }

  ngOnInit() {
  }

}
