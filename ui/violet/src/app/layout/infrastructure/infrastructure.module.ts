import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { InfrastructureRoutingModule } from './infrastructure-routing.module';
import { InfrastructureComponent } from './infrastructure.component';
import { PageHeaderModule } from './../../shared';

@NgModule({
    imports: [CommonModule, InfrastructureRoutingModule, PageHeaderModule],
    declarations: [InfrastructureComponent]
})
export class InfrastructureModule {}
