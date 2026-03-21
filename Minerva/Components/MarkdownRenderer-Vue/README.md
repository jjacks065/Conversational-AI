# JSON Markdown Viewer - Vue.js

A simple Vue.js web application for rendering JSON responses with markdown content.

## Features

- **JSON Input**: Paste JSON responses containing markdown content
- **Real-time Rendering**: Instantly see rendered markdown using Vue's reactivity
- **Error Handling**: Clear error messages for invalid JSON
- **Sample Data**: Built-in sample data for testing
- **Responsive Design**: Works on desktop and mobile devices
- **Vue 3 Composition API**: Modern Vue.js architecture

## Usage

1. **Start the Application**:
   ```bash
   npm run dev
   ```
   The app will run at `http://localhost:4300`

2. **Input JSON Data**:
   - Paste your JSON response in the input textarea
   - The JSON should contain a `content` field with markdown text
   - Click "Load Sample" to see an example

3. **View Results**:
   - The rendered markdown appears in the preview section
   - Raw markdown content can be viewed by expanding the details section

## Expected JSON Format

```json
{
  "questionId": "unique-id",
  "sessionId": "session-id", 
  "content": "**Your markdown content here**\\n\\nWith proper formatting...",
  "responseId": "response-id"
}
```

## Supported Markdown Features

- Headers (`##`, `###`)
- Bold text (`**text**`)
- Tables
- Lists (ordered and unordered)
- Line breaks (`\\n`)
- Paragraph breaks (`\\n\\n`)
- Horizontal rules (`---`)

## Sample Files

Sample JSON files are available in the `sample-data/` directory:
- `sample-response.json` - Sample health insurance response
- `simple-example.json` - Basic markdown features demonstration

## Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Technology Stack

- **Vue 3**: Modern reactive framework with Composition API
- **Vite**: Fast build tool and development server
- **Marked**: Markdown parsing and rendering
- **JavaScript ES6+**: Modern JavaScript features
- **CSS**: Responsive styling

## Project Structure

```
src/
├── components/
│   └── JsonMarkdownViewer.vue  # Main component
├── App.vue                     # Root component
├── main.js                     # Application entry point
└── style.css                   # Global styles
sample-data/
├── sample-response.json        # Sample data files
└── simple-example.json
```

## Comparison with Angular Version

This Vue.js version provides the same functionality as the Angular version but with:
- Vue 3 Composition API for reactive state management
- Vite for faster development and builds
- Simpler component structure
- Smaller bundle size
- Different port (4300) to run alongside Angular version

## Browser Support

- Modern evergreen browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Requires ES6+ support