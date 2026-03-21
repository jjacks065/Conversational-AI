<template>
  <div class="json-viewer-container">
    <!-- Superscript Toggle -->
    <div class="card toggle-section">
      <div class="toggle-container">
        <label class="toggle-label">
          <input 
            type="checkbox" 
            v-model="enableCitationSuperscript" 
            @change="onJsonInputChange"
            class="toggle-checkbox"
          />
          <span class="toggle-text">Enable Citation Superscript</span>
          <span class="toggle-description">Transform [1], [2], etc. into superscript citations</span>
        </label>
      </div>
    </div>

    <!-- Input Section -->
    <div class="card">
      <div class="input-header">
        <h2>JSON Input</h2>
        <div class="button-group">
          <button class="btn btn-secondary" @click="loadSampleData">Load Sample</button>
          <button class="btn btn-secondary" @click="clearInput">Clear</button>
        </div>
      </div>
      
      <textarea
        v-model="jsonInput"
        @input="onJsonInputChange"
        class="json-input"
        placeholder="Paste your JSON response here..."
        rows="12"
      ></textarea>
      
      <div v-if="errorMessage" class="error-message">
        <strong>Error:</strong> {{ errorMessage }}
      </div>
    </div>

    <!-- Preview Section -->
    <div v-if="showPreview" class="card">
      <h2>Rendered Markdown</h2>
      <div class="markdown-content" v-html="renderedMarkdown"></div>
    </div>

    <!-- Raw Content Section (optional, for debugging) -->
    <div v-if="showPreview && parsedContent" class="card">
      <details>
        <summary><strong>Raw Markdown Content</strong> (click to expand)</summary>
        <pre class="raw-content">{{ parsedContent }}</pre>
      </details>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { marked } from 'marked'

export default {
  name: 'JsonMarkdownViewer',
  setup() {
    const jsonInput = ref('')
    const parsedContent = ref('')
    const renderedMarkdown = ref('')
    const errorMessage = ref('')
    const showPreview = ref(false)
    const enableCitationSuperscript = ref(true) // Default to enabled

    const configureMarked = () => {
      if (enableCitationSuperscript.value) {
        // Configure marked with custom citation renderer
        const renderer = new marked.Renderer()
        
        // Custom renderer for text to handle citations as superscript
        renderer.text = function(text) {
          // Replace square bracket patterns [number] or [text] with superscript
          return text.replace(/\[([^\]]+)\]/g, '<sup>[$1]</sup>')
        }
        
        marked.setOptions({
          breaks: true,
          gfm: true,
          renderer: renderer
        })
      } else {
        // Use default marked configuration without custom renderer
        marked.setOptions({
          breaks: true,
          gfm: true,
          renderer: new marked.Renderer() // Reset to default renderer
        })
      }
    }

    // Initial configuration
    configureMarked()

    const onJsonInputChange = () => {
      // Reconfigure marked based on current toggle state
      configureMarked()
      
      errorMessage.value = ''
      showPreview.value = false
      
      if (!jsonInput.value.trim()) {
        parsedContent.value = ''
        renderedMarkdown.value = ''
        return
      }

      try {
        const parsed = JSON.parse(jsonInput.value)
        
        if (!parsed.content) {
          errorMessage.value = 'JSON does not contain a "content" field'
          return
        }

        parsedContent.value = parsed.content
        renderedMarkdown.value = marked(parsedContent.value)
        showPreview.value = true
      } catch (error) {
        errorMessage.value = 'Invalid JSON format: ' + error.message
      }
    }

    const loadSampleData = () => {
      // Load sample data based on the provided JSON files
      const sampleJson = {
        "questionId": "87b89b5d-7c70-41c0-9568-db6ebc7dc3f4",
        "sessionId": "a3b36bda-db02-4614-b2a9-f398671ab392",
        "content": "**Brief Answer**  \\nYes—this plan includes Pregnancy and Maternity Care benefits (prenatal care, postnatal care, complications of pregnancy, and inpatient hospital services for labor/delivery/postpartum). Your cost share depends on where services are provided and whether they are professional vs. facility charges.\\n\\n---\\n**Detailed Explanation**\\n\\n### Pregnancy and Maternity Care (general)\\nPregnancy and maternity care benefits include:\\n\\nPrenatal care;  \\nPostnatal care;  \\nInvoluntary complications of pregnancy;  \\nInpatient Hospital services including labor, delivery, and postpartum care\\n\\n### Cost Structure\\n- **In-Network**: Lower deductibles and coinsurance\\n- **Out-of-Network**: Higher deductibles and coinsurance\\n\\n| Service Type | In-Network | Out-of-Network |\\n|-------------|------------|----------------|\\n| Pre/Postnatal Visits | No Charge | 40% Coinsurance |\\n| Delivery - Hospital | 20% Coinsurance | 40% Coinsurance |\\n| Delivery - Professional | 20% Coinsurance | 40% Coinsurance |",
        "responseId": "resp_sample_vue"
      }
      
      jsonInput.value = JSON.stringify(sampleJson, null, 2)
      onJsonInputChange()
    }

    const clearInput = () => {
      jsonInput.value = ''
      parsedContent.value = ''
      renderedMarkdown.value = ''
      errorMessage.value = ''
      showPreview.value = false
    }

    return {
      jsonInput,
      parsedContent,
      renderedMarkdown,
      errorMessage,
      showPreview,
      enableCitationSuperscript,
      onJsonInputChange,
      loadSampleData,
      clearInput
    }
  }
}
</script>

<style scoped>
.json-viewer-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toggle-section {
  border-left: 4px solid #667eea;
  background: linear-gradient(135deg, #f8fafc, #e0e7ff);
}

.toggle-container {
  display: flex;
  align-items: center;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-weight: 500;
}

.toggle-checkbox {
  width: 18px;
  height: 18px;
  accent-color: #667eea;
  cursor: pointer;
}

.toggle-text {
  font-size: 16px;
  color: #333;
}

.toggle-description {
  font-size: 14px;
  color: #666;
  font-style: italic;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.input-header h2 {
  margin: 0;
  color: #333;
}

.button-group {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.json-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.4;
  resize: vertical;
  min-height: 200px;
  white-space: nowrap;
  overflow-x: auto;
}

.json-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

.markdown-content {
  line-height: 1.6;
  color: #333;
}

/* Custom styling for citations as superscript */
.markdown-content sup {
  font-size: 0.75em;
  font-weight: 500;
  color: #0066cc;
  cursor: help;
  text-decoration: none;
  border-radius: 2px;
  padding: 1px 2px;
  background: rgba(0, 102, 204, 0.1);
  border: 1px solid rgba(0, 102, 204, 0.2);
  margin: 0 1px;
}

.markdown-content sup:hover {
  background: rgba(0, 102, 204, 0.15);
  border-color: rgba(0, 102, 204, 0.3);
}

.raw-content {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 12px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.4;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin-top: 10px;
}

details {
  margin-top: 10px;
}

details summary {
  cursor: pointer;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  color: #667eea;
}

details summary:hover {
  color: #5a6cdb;
}

/* Layout remains stacked vertically for all screen sizes */
</style>