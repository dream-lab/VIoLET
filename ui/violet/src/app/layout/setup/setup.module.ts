import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SetupComponent } from './setup.component';
import { SetupRoutingModule } from './setup-routing.module';
import { PageHeaderModule } from './../../shared';

@NgModule({
    imports: [CommonModule, PageHeaderModule, SetupRoutingModule],
    declarations: [SetupComponent]
})
export class SetupModule {}
