# Roadmap Generator System

## Overview

This system generates **self-contained HTML roadmap presentations** from JSON data. No servers, no CORS issues, no external dependencies - just double-click to present!

## 🚀 **Quick Start**

```bash
# 1. Make sure you have a JSON file with roadmap data
# 2. Generate your presentation
./quick-generate.sh

# 3. Double-click the generated HTML file to present!
```

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

### 🚀 **Quick Start (Recommended)**

```bash
# Generate presentation-ready roadmap (one command)
./quick-generate.sh

# Or specify a different directory
./quick-generate.sh /path/to/your/data
```

### 📋 **Standard Usage**

```bash
# Generate roadmap from current directory
python3 generate-roadmap.py .

# Generate from specific directory
python3 generate-roadmap.py /path/to/data

# Custom output name
python3 generate-roadmap.py . -o my-custom-roadmap.html

# Use different template
python3 generate-roadmap.py . -t /path/to/template.html
```

### ✨ **What It Does**

1. **Reads** your `roadmap-data.json` file
2. **Embeds** all data directly into the HTML template  
3. **Generates** a self-contained HTML file
4. **Names** the file based on your roadmap title
5. **Ready** to open in any browser - no server required!

### 📄 **Output Example**

- **Input**: `roadmap-data.json` with title "CSR Chat Roadmap 2026-2027"
- **Output**: `csr-chat-roadmap-2026-2027.html` (fully self-contained)
- **Result**: Double-click to open, works in any browser!

### Quick Updates
To update roadmap content:
1. Edit `roadmap-data.json` with your changes
2. Run `./quick-generate.sh` to regenerate
3. Share the new HTML file

> **Advantage**: No more CORS issues, no server needed, perfect for presentations and sharing!

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

### Common Updates

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

## Deployment

**✨ New Approach: Self-Contained Files**

The generated HTML files are completely self-contained and work everywhere:

- ✅ **Double-click** to open in any browser
- ✅ **Email** or share via file transfer
- ✅ **Upload** to any web hosting
- ✅ **Present** offline without internet
- ✅ **Works** on all operating systems

**File Requirements:**
- JSON data file (any ".json" file in the directory)
- Stellarus logo file: `Stellarus_logo_2C_whiteype.png` (optional)
- Generator creates everything else automatically

**No Server Required!** 🎉

## Troubleshooting

**Generation Issues:**
- **No JSON file found**: Ensure you have a `.json` file in your directory
- **Invalid JSON**: Run `python3 validate-roadmap.py` to check syntax
- **Template not found**: Ensure `Roadmap-Template.html` exists in the same directory as the generator

**Display Issues:**
- **Logo not showing**: Check that `Stellarus_logo_2C_whiteype.png` is in the same directory
- **Broken styling**: Ensure you didn't modify the template structure
- **Content missing**: Validate your JSON file structure

**Generator Options:**
```bash
# See all options
python3 generate-roadmap.py --help

# Generate with custom output name
python3 generate-roadmap.py . -o my-roadmap.html

# Use different template
python3 generate-roadmap.py . -t custom-template.html
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