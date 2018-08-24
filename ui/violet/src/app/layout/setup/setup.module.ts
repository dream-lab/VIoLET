import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SetupComponent } from './setup.component';
import { SetupRoutingModule } from './setup-routing.module';
import { PageHeaderModule } from './../../shared';
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import {AceEditorModule} from "ng2-ace-editor";
import {ImageViewerModule} from "ng2-image-viewer";
import {SetupInfraComponent} from "./setup-infra/setup-infra.component";
import {SetupPartitionComponent} from "./setup-partition/setup-partition.component";
import {SetupDeploymentComponent} from "./setup-deployment/setup-deployment.component";
import {SetupSanityComponent} from "./setup-sanity/setup-sanity.component";
import {PdfViewerModule} from "ng2-pdf-viewer";

@NgModule({
    imports: [CommonModule, PageHeaderModule, SetupRoutingModule, FormsModule, NgbModule.forRoot(), AceEditorModule, PdfViewerModule, ImageViewerModule],
    declarations: [SetupComponent, SetupInfraComponent, SetupPartitionComponent, SetupDeploymentComponent, SetupSanityComponent]
})
export class SetupModule {}
