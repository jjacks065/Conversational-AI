import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { JsonMarkdownViewerComponent } from './json-markdown-viewer/json-markdown-viewer.component';

@NgModule({
  declarations: [
    AppComponent,
    JsonMarkdownViewerComponent
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }