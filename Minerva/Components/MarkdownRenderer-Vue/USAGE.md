# Using the JSON Markdown Viewer - Vue.js

## Quick Start

1. **Open the Application**: Navigate to `http://localhost:4300` in your browser
2. **Test with Sample Data**: Click "Load Sample" to see a working example
3. **Try Your Own JSON**: Paste your JSON response in the input area

## Step-by-Step Instructions

### Option 1: Use Built-in Sample
1. Click the "Load Sample" button
2. See the rendered markdown appear below the input
3. Expand "Raw Markdown Content" to see the original text

### Option 2: Use Sample Files
1. Open one of the sample files:
   - `sample-data/simple-example.json` - Basic markdown features
   - `sample-data/sample-response.json` - Complex health insurance example
2. Copy the entire JSON content
3. Paste it into the input textarea
4. Watch the markdown render automatically via Vue's reactivity

### Option 3: Use Your Own Data
1. Copy your JSON response (must have a "content" field)
2. Paste into the input area
3. View the rendered result instantly

## Sample JSON Structure

Your JSON should look like this:
```json
{
  "questionId": "your-question-id",
  "sessionId": "your-session-id", 
  "content": "Your **markdown** content here\\n\\n## With proper formatting",
  "responseId": "your-response-id"
}
```

## Vue.js Specific Features

- **Reactive Updates**: Changes to input are instantly reflected
- **Composition API**: Modern Vue 3 architecture
- **v-model**: Two-way data binding for textarea
- **v-if/v-show**: Conditional rendering for error messages and preview
- **Template Syntax**: Clean, declarative templates

## Development Commands

```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview
```

## Troubleshooting

**Error: "Invalid JSON format"**
- Check that your JSON is properly formatted
- Ensure all quotes are properly escaped
- Validate JSON syntax

**Error: "JSON does not contain a content field"**
- Make sure your JSON has a "content" property
- Check that the content field contains your markdown text

**Markdown not rendering correctly**
- Ensure you're using proper markdown syntax
- Use `\\n` for line breaks in JSON
- Use `\\n\\n` for paragraph breaks

**Port conflict with Angular version**
- Vue version runs on port 4300
- Angular version runs on port 4200
- Both can run simultaneously for comparison

## Vue Development Tips

- **Hot Reload**: Vite provides instant updates during development
- **Vue DevTools**: Install browser extension for debugging
- **Composition API**: Check the component setup() function for reactive state
- **Template Debugging**: Use {{ }} interpolation to debug values

## Supported Markdown Features

✅ **Headers**: `##`, `###`  
✅ **Bold text**: `**text**`  
✅ **Tables**: Standard markdown tables  
✅ **Lists**: Both ordered and unordered  
✅ **Line breaks**: `\\n` in JSON  
✅ **Paragraphs**: `\\n\\n` in JSON  
✅ **Horizontal rules**: `---`  
✅ **Reactive rendering**: Instant updates with Vue

## Tips

- Use the "Clear" button to reset the input
- Click "Load Sample" anytime to see a working example
- The raw content section helps debug formatting issues
- The app automatically updates as you type thanks to Vue reactivity
- Compare with Angular version running on port 4200