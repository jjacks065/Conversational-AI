# Minerva API Response Validation Page

This is a React-based validation tool for testing Minerva API responses by converting them to clean HTML using markdown rendering.

## Features

- **Real-time Markdown Rendering**: Input raw API response text and see it rendered as clean HTML instantly
- **Sample Data Loading**: Built-in buttons to load sample responses for testing
- **Responsive Design**: Side-by-side layout on desktop, stacked layout on mobile
- **Clean HTML Output**: Uses react-markdown with rehype-raw plugin for comprehensive markdown-to-HTML conversion

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm

### Installation

1. Navigate to the project directory:

   ```bash
   cd /Users/jjacks20/jjacks/Conversational-AI/Minerva/validation-page
   ```
2. Install dependencies:

   ```bash
   npm install
   ```
3. Start the development server:

   ```bash
   npm run dev
   ```

# Minerva API Response Validation Page

This is a React-based validation tool for testing Minerva API responses by converting them to clean HTML using markdown rendering.

## Features

- **Real-time Markdown Rendering**: Input raw API response text and see it rendered as clean HTML instantly
- **Sample Data Loading**: Built-in buttons to load sample responses for testing
- **Responsive Design**: Side-by-side layout on desktop, stacked layout on mobile
- **Clean HTML Output**: Uses react-markdown with rehype-raw plugin for comprehensive markdown-to-HTML conversion

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm

### Installation

1. Navigate to the project directory:

   ```bash
   cd /Users/jjacks20/jjacks/Conversational-AI/Minerva/validation-page
   ```
2. Install dependencies:

   ```bash
   npm install
   ```
3. Start the development server:

   ```bash
   npm run dev
   ```
4. Open your browser to the URL shown in the terminal (typically http://localhost:5173)

## Usage

1. **Manual Input**: Paste any API response text into the left textarea
2. **Sample Data**: Use the "Load Urgent Care Sample" or "Load Maternity Sample" buttons to test with real API response examples
3. **Clear**: Use the "Clear" button to reset the input
4. **View Results**: The right panel shows the rendered HTML output in real-time

## Components

- **ValidationPage**: Main component with input/output panes and sample data controls
- **React Markdown**: Renders markdown text to clean HTML
- **Rehype Raw**: Plugin to handle raw HTML within markdown

## Sample Data

The validation page includes two sample API responses:

1. **Urgent Care Sample**: Healthcare plan urgent care and emergency room benefits
2. **Maternity Sample**: Pregnancy and maternity care benefits with detailed cost sharing information

## Dependencies

Key dependencies include:

- **React 19.2.4**: Core React framework
- **react-markdown 9.0.1**: Markdown to HTML rendering
- **rehype-raw 7.0.0**: Plugin for handling raw HTML in markdown
- **Vite 8.0.0**: Development server and build tool

## File Structure

```
src/
├── components/
│   ├── ValidationPage.jsx    # Main validation component
│   └── ValidationPage.css    # Component styles
├── App.jsx                   # Root application component
├── App.css                   # Application styles
└── main.jsx                  # Application entry point
```
