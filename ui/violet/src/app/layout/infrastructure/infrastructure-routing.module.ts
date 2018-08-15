import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { InfrastructureComponent } from './infrastructure.component';

const routes: Routes = [
    {
        path: '', component: InfrastructureComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class InfrastructureRoutingModule {
}
