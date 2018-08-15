import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../router.animations';
import {InfrastructureModel} from "./infrastructure.model";

@Component({
    selector: 'app-form',
    templateUrl: './infrastructure.component.html',
    styleUrls: ['./infrastructure.component.scss'],
    animations: [routerTransition()]
})
export class InfrastructureComponent implements OnInit {

    infra = new InfrastructureModel();

    constructor() {}

    ngOnInit() {}

    logger() {
        console.log(this.infra.devices);
    }
}
