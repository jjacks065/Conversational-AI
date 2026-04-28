# Minerva Platform Roadmap Template System

## Overview

This template system separates the roadmap presentation from the content data, making it easy to update plans and strategy without touching the HTML or styling code.

## Files Structure

### Core Files
- `Roadmap-Template.html` - The HTML template for roadmap presentations
- `roadmap-data.json` - All roadmap content in structured JSON format
- `generate-roadmap.py` - **Main generator script** - creates self-contained HTML files
- `quick-generate.sh` - One-click generation script

### Utilities
- `validate-roadmap.py` - Validation utility for JSON structure
- `update-roadmap.py` - Interactive utility for common updates
- `README.md` - This documentation file
- `SAMPLE-UPDATES.md` - Examples of common roadmap modifications

## Usage

### Quick Updates
To update roadmap content:
1. Edit `roadmap-data.json` with your changes
2. Open `Minerva-Platform-Roadmap-Template.html` in a browser
3. The presentation will automatically load the updated data

## Data Structure

The JSON file has the following main sections:

#### Metadata
```json
{
  "metadata": {
    "title": "Page title for browser tab",
    "pageTitle": "Main header title", 
    "logoPath": "Path to Stellarus logo",
    "disclaimer": "Confidential disclaimer text",
    "theme": {
      "primaryGradient": "CSS gradient for background",
      "accentColor": "Accent color for highlights"
    }
  }
}
```

#### Navigation
```json
{
  "navigation": [
    {"id": 0, "label": "Overview", "section": "overview"}
  ]
}
```

#### Sections
Each section corresponds to a navigation item:

- **overview**: Strategic metrics, transformation description, quarter overview
- **q2-details**: Detailed Q2 implementation cards with features
- **q3-q1-roadmap**: Future quarters roadmap with objectives 
- **metrics**: Success metrics, KPIs, and risk mitigation

## Common Updates

#### Adding New Metrics
In the `overview.metrics` array:
```json
{
  "type": "metric-type",
  "value": "Display value", 
  "label": "Metric label",
  "icon": "📊"
}
```

#### Adding Q2 Features
In the `q2-details.cards` array, add features to any card:
```json
{
  "name": "Feature Name",
  "description": "Feature description text"
}
```

#### Updating Quarter Plans
In the `q3-q1-roadmap.quarters` array:
```json
{
  "quarter": "Q3 2026",
  "theme": "Quarter Theme", 
  "subtitle": "Subtitle text",
  "objectives": ["Objective 1", "Objective 2"]
}
```

#### Managing Success Metrics
In the `metrics` section, update the KPIs:
```json
{
  "type": "cost-down",
  "label": "Metric Label",
  "value": "Target Value", 
  "detail": "Additional context",
  "icon": "📉"
}
```

### Template Features

- **Responsive Design**: Works on desktop and mobile
- **Brand Compliance**: Stellarus colors, typography, and logo
- **Interactive Navigation**: Section-based presentation flow
- **Smooth Animations**: Professional transitions and hover effects
- **Error Handling**: Graceful fallback if JSON file is missing

### Deployment

1. Ensure both HTML and JSON files are in the same directory
2. Ensure the Stellarus logo file is accessible at the specified path
3. Open the HTML file in any modern web browser
4. For presentations, use fullscreen mode (F11)

### Troubleshooting

**Blank Page**: Check browser console for errors. Ensure JSON file is valid and accessible.

**Logo Not Showing**: Verify the logo path in `metadata.logoPath` is correct relative to the HTML file.

**Content Not Loading**: Ensure JSON syntax is valid. Use a JSON validator if needed.

## Utilities

### 🔧 **Generation Tools**
```bash
# Quick generation (easiest)
./quick-generate.sh

# Full-featured generator
python3 generate-roadmap.py . [options]

# List available JSON files
python3 generate-roadmap.py . --list-json
```

### ✅ **Validation Tool**
```bash
python3 validate-roadmap.py
```
Validates the JSON structure and reports any missing required fields or formatting issues.

### 🎛️ **Interactive Update Tool**
```bash
python3 update-roadmap.py
```
Interactive utility for common updates:
- Add overview metrics
- Add Q2 features to existing cards
- Add objectives to quarters
- Add success metrics
- Guided prompts with validation

### 🔄 **Complete Workflow**
```bash
# 1. Make changes to roadmap-data.json
# 2. Validate the changes
python3 validate-roadmap.py
# 3. Generate new presentation
./quick-generate.sh
# 4. Share the generated HTML file
```

## Development Notes

### Generator Architecture
- **Template-based**: Uses `Roadmap-Template.html` as the base structure
- **Data Embedding**: Injects JSON data directly into JavaScript variables
- **Self-contained**: No external dependencies or network requests
- **Cross-platform**: Works on Windows, Mac, and Linux

### Template System
- **Vanilla JavaScript**: Maximum compatibility, no frameworks required
- **Modern CSS**: Grid and Flexbox with fallbacks for older browsers
- **Brand Compliant**: Maintains Stellarus guidelines (colors, typography, logos)
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### File Naming
- Output files use sanitized version of the `metadata.title` field
- Spaces become dashes, special characters removed
- Example: "CSR Chat Roadmap 2026-2027" → `csr-chat-roadmap-2026-2027.html`