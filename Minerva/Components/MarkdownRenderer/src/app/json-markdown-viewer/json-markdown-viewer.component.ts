import { Component } from '@angular/core';
import { marked } from 'marked';

interface ApiResponse {
  questionId: string;
  sessionId: string;
  content: string;
  responseId: string;
}

@Component({
  selector: 'app-json-markdown-viewer',
  templateUrl: './json-markdown-viewer.component.html',
  styleUrls: ['./json-markdown-viewer.component.css']
})
export class JsonMarkdownViewerComponent {
  jsonInput: string = '';
  parsedContent: string = '';
  renderedMarkdown: string = '';
  errorMessage: string = '';
  showPreview: boolean = false;
  enableCitationSuperscript: boolean = true; // Default to enabled

  constructor() {
    // Initial marked configuration
    this.configureMarked();
  }

  private configureMarked(): void {
    if (this.enableCitationSuperscript) {
      // Configure marked with custom citation renderer
      const renderer = new marked.Renderer();
      
      // Custom renderer for text to handle citations as superscript
      renderer.text = function(text: string) {
        // Replace square bracket patterns [number] or [text] with superscript
        return text.replace(/\[([^\]]+)\]/g, '<sup>[$1]</sup>');
      };
      
      marked.setOptions({
        breaks: true,
        gfm: true,
        renderer: renderer
      });
    } else {
      // Use default marked configuration without custom renderer
      marked.setOptions({
        breaks: true,
        gfm: true,
        renderer: new marked.Renderer() // Reset to default renderer
      });
    }
  }

  onToggleChange(): void {
    this.configureMarked();
    // Re-render if content exists
    if (this.parsedContent) {
      this.renderedMarkdown = marked(this.parsedContent) as string;
    }
  }

  onJsonInputChange(): void {
    this.errorMessage = '';
    this.showPreview = false;
    
    if (!this.jsonInput.trim()) {
      this.parsedContent = '';
      this.renderedMarkdown = '';
      return;
    }

    try {
      const parsed: ApiResponse = JSON.parse(this.jsonInput);
      
      if (!parsed.content) {
        this.errorMessage = 'JSON does not contain a "content" field';
        return;
      }

      this.parsedContent = parsed.content;
      this.renderedMarkdown = marked(this.parsedContent) as string;
      this.showPreview = true;
    } catch (error) {
      this.errorMessage = 'Invalid JSON format: ' + (error as Error).message;
    }
  }

  loadSampleData(): void {
    // Load sample data based on the provided JSON files
    const sampleJson: ApiResponse = {
      "questionId": "87b89b5d-7c70-41c0-9568-db6ebc7dc3f4",
      "sessionId": "a3b36bda-db02-4614-b2a9-f398671ab392",
      "content": "**Brief Answer**  \\nYes—this plan includes Pregnancy and Maternity Care benefits (prenatal care, postnatal care, complications of pregnancy, and inpatient hospital services for labor/delivery/postpartum). Your cost share depends on where services are provided and whether they are professional vs. facility charges.\\n\\n---\\n**Detailed Explanation**\\n\\n### Pregnancy and Maternity Care (general)\\nPregnancy and maternity care benefits include:\\n\\nPrenatal care;  \\nPostnatal care;  \\nInvoluntary complications of pregnancy;  \\nInpatient Hospital services including labor, delivery, and postpartum care\\n\\n### Cost Structure\\n- **In-Network**: Lower deductibles and coinsurance\\n- **Out-of-Network**: Higher deductibles and coinsurance\\n\\n| Service Type | In-Network | Out-of-Network |\\n|-------------|------------|----------------|\\n| Pre/Postnatal Visits | No Charge | 40% Coinsurance |\\n| Delivery - Hospital | 20% Coinsurance | 40% Coinsurance |\\n| Delivery - Professional | 20% Coinsurance | 40% Coinsurance |",
      "responseId": "resp_sample"
    };
    
    this.jsonInput = JSON.stringify(sampleJson, null, 2);
    this.onJsonInputChange();
  }

  clearInput(): void {
    this.jsonInput = '';
    this.parsedContent = '';
    this.renderedMarkdown = '';
    this.errorMessage = '';
    this.showPreview = false;
  }
}