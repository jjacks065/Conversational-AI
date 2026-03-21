import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div class="container">
      <header class="card">
        <h1>JSON Markdown Viewer</h1>
        <p>Paste your JSON response to render the markdown content below.</p>
      </header>
      <app-json-markdown-viewer></app-json-markdown-viewer>
    </div>
  `,
  styles: [`
    header {
      text-align: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    
    header h1 {
      margin: 0 0 10px 0;
      font-size: 2.5rem;
    }
    
    header p {
      margin: 0;
      opacity: 0.9;
    }
  `]
})
export class AppComponent {
  title = 'json-markdown-viewer';
}