import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SetupComponent } from './setup.component';
import { SetupRoutingModule } from './setup-routing.module';
import { PageHeaderModule } from './../../shared';
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {AceEditorModule} from "ng2-ace-editor";
import {NgxJsonViewerModule} from "ngx-json-viewer";

@NgModule({
    imports: [CommonModule, PageHeaderModule, SetupRoutingModule, FormsModule, NgbModule.forRoot(), AceEditorModule,
              NgxJsonViewerModule],
    declarations: [SetupComponent]
})
export class SetupModule {}
