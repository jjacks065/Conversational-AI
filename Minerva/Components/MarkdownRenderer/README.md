# JSON Markdown Viewer

A simple Angular web application for rendering JSON responses with markdown content.

## Features

- **JSON Input**: Paste JSON responses containing markdown content
- **Real-time Rendering**: Instantly see rendered markdown as you type/paste
- **Error Handling**: Clear error messages for invalid JSON
- **Sample Data**: Built-in sample data for testing
- **Responsive Design**: Works on desktop and mobile devices

## Usage

1. **Start the Application**:
   ```bash
   npm start
   ```
   The app will run at `http://localhost:4200`

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

Sample JSON files are available in the `../Background/` directory:
- `Response.JSON` - Sample health insurance response
- `Response2.JSON` - Additional sample response

## Installation

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Technology Stack

- **Angular 17**: Modern web framework
- **Marked**: Markdown parsing and rendering
- **TypeScript**: Type-safe development
- **CSS**: Responsive styling

## Browser Support

- Modern evergreen browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)