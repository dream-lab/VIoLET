import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SetupComponent } from './setup.component';
import { SetupRoutingModule } from './setup-routing.module';
import { PageHeaderModule } from './../../shared';

@NgModule({
    imports: [CommonModule, PageHeaderModule, SetupRoutingModule, FormsModule],
    declarations: [SetupComponent]
})
export class SetupModule {}
