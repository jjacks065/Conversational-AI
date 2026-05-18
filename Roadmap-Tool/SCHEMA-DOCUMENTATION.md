# Roadmap JSON Schema Documentation

## Overview

The `roadmap-schema.json` file defines the official JSON Schema contract for all Stellarus roadmap documents. This schema ensures consistency, validation, and proper structure across all roadmap presentations.

## Purpose

1. **Validation**: Automatically validate roadmap JSON documents before generation
2. **Documentation**: Serve as authoritative documentation for the roadmap data structure
3. **IDE Support**: Enable autocomplete and validation in modern code editors
4. **Quality Assurance**: Prevent structural errors and missing required fields

## Schema Version

- **Schema Draft**: JSON Schema Draft-07
- **Schema ID**: `https://stellarus.com/schemas/roadmap-v1.json`
- **File**: `roadmap-schema.json`

---

## Required Top-Level Properties

Every roadmap document must include:

```json
{
  "metadata": { ... },     // Presentation configuration
  "navigation": [ ... ],   // Navigation menu items  
  "sections": { ... }      // Content sections
}
```

---

## 1. Metadata Structure

**Required Fields:**
- `title` (string): Browser tab title (1-200 chars)
- `pageTitle` (string): Main page header (1-300 chars, supports emoji/HTML)
- `disclaimer` (string): Confidentiality notice (1-500 chars)
- `theme` (object): Visual theme configuration

**Optional Fields:**
- `logoPath` (string): Relative path to logo (must match pattern: `./path/file.{png|jpg|jpeg|svg|gif}`)
- `version` (string): Version identifier (format: `1.0` or `1.0-Internal`)
- `lastUpdated` (string): Date in YYYY-MM-DD format

### Theme Object

**Required:**
- `primaryGradient` (string): CSS gradient (must start with `linear-gradient` or `radial-gradient`)
- `accentColor` (string): Hex color code (format: `#RRGGBB`)

**Optional:**
- `costColor` (string): Hex color for cost elements
- `warningColor` (string): Hex color for warnings

**Example:**
```json
{
  "metadata": {
    "title": "CSR Chat Roadmap 2026-2027",
    "pageTitle": "🚀 CSR Chat Platform Evolution",
    "logoPath": "./Stellarus_logo_2C_whiteype.png",
    "disclaimer": "🔒 INTERNAL USE ONLY - CONFIDENTIAL",
    "theme": {
      "primaryGradient": "linear-gradient(135deg, #08285E 0%, #436DB3 100%)",
      "accentColor": "#F4454E",
      "costColor": "#2ECC71",
      "warningColor": "#F39C12"
    },
    "version": "2.0-Internal",
    "lastUpdated": "2026-05-06"
  }
}
```

---

## 2. Navigation Array

Array of navigation items linking to sections.

**Required Fields per Item:**
- `id` (integer): Unique identifier (>= 0)
- `label` (string): Display text (1-50 chars)
- `section` (string): Section ID (must match a key in `sections` object, lowercase with hyphens only)

**Example:**
```json
{
  "navigation": [
    {"id": 0, "label": "Overview", "section": "overview"},
    {"id": 1, "label": "Q2 Details", "section": "q2-details"},
    {"id": 2, "label": "Q3-Q1", "section": "q3-q1-roadmap"},
    {"id": 3, "label": "Metrics", "section": "metrics"}
  ]
}
```

**Validation Rules:**
- Navigation IDs must be unique
- Section references must exist in the `sections` object
- Section IDs must use lowercase letters, numbers, and hyphens only

---

## 3. Sections Object

Dynamic object where keys are section IDs and values are section content.

**Required per Section:**
- `title` (string): Section heading (1-200 chars)

**Common Section Properties:**

### Metrics Array
Direct array of metrics for the section:
```json
{
  "metrics": [
    {
      "type": "accuracy",
      "value": ">98%",
      "label": "Accuracy Target",
      "icon": "✅",
      "costImpact": "Optional cost description"
    }
  ]
}
```

**Required Fields per Metric:**
- `value` (string): Metric value
- `label` (string): Display label (1-100 chars)
- `icon` (string): Emoji or icon (1-10 chars)

**Optional Metric Fields:**
- `type`, `detail`, `costImpact`, `costImplication`
- Quarterly targets: `q2Target`, `q3Target`, `q4Target`, `q1'27Target`
- Quarterly values: `q2`, `q3`, `q4`, `q1'27`, `annual`
- Timeline: `baseline`, `improvement`, `paybackMonth`
- Endpoints: `q2End`, `q3End`, `q4End`, `q1'27End`, `q1Baseline`

### Transformation Object
Vision and strategy description:
```json
{
  "transformation": {
    "title": "Strategic Transformation",
    "description": "Transform platform from X to Y (supports HTML)"
  }
}
```

### Quarter Overview Object
High-level quarter themes:
```json
{
  "quarterOverview": {
    "title": "Year Overview",
    "quarters": [
      {
        "quarter": "Q2 2026",
        "subheader": "Foundation",
        "description": "Build core capabilities",
        "budget": "$285,000",
        "costPerRequest": "$0.18",
        "projectedSavings": "$450,000",
        "roi": "158%"
      }
    ]
  }
}
```

**Required per Quarter:**
- `quarter` (string): Format `Q[1-4] YYYY`
- `subheader` (string): Theme
- `description` (string): Details

**Optional:** `budget`, `costPerRequest`, `projectedSavings`, `roi`

### Financial Summary Object
Financial impact overview:
```json
{
  "financialSummary": {
    "title": "Financial Impact",
    "totalInvestment": "$1,100,000",
    "projectedSavings": "$4,200,000",
    "netBenefit": "$3,100,000",
    "paybackPeriod": "3.2 months",
    "breakdown": [
      {
        "category": "Infrastructure",
        "amount": "$480,000",
        "percentage": "44%"
      }
    ]
  }
}
```

### Cards Array
Feature or initiative cards (typically for Q2 details):
```json
{
  "cards": [
    {
      "title": "🚀 Performance Improvements",
      "color": "#ff6b6b",
      "target": "63% response time reduction",
      "scope": "Optional scope description",
      "budget": "$85,000",
      "costMetrics": {
        "infrastructure": "$35,000",
        "engineering": "$40,000"
      },
      "costBenefit": {
        "monthlySavings": "$150,000",
        "roi": "529%"
      },
      "features": [
        {
          "name": "Feature Name",
          "description": "Description (supports HTML lists)",
          "costDrivers": "Optional cost breakdown",
          "costSavings": "Optional savings details"
        }
      ]
    }
  ]
}
```

**Required per Card:**
- `title` (string): Card heading
- `color` (string): Hex color `#RRGGBB`
- `features` (array): At least one feature

**Required per Feature:**
- `name` (string): Feature name
- `description` (string): Feature details

### Quarters Array
Quarterly roadmap (typically for Q3-Q1 section):
```json
{
  "quarters": [
    {
      "quarter": "Q3 2026",
      "theme": "Growth & Scale",
      "subtitle": "Platform expansion",
      "budget": "$320,000",
      "costPerRequest": "$0.12",
      "projectedSavings": "$1,200,000",
      "roi": "275%",
      "objectives": [
        "Simple objective string",
        {
          "title": "💊 Formulary Integration",
          "description": "Comprehensive formulary intelligence",
          "alignment": "🤝 Phase 2",
          "budget": "$110,000",
          "costBreakdown": {
            "integration": "$45,000"
          },
          "costBenefit": {
            "monthlySavings": "$120,000"
          },
          "initiatives": [
            "Real-time formulary lookup",
            "Drug coverage intelligence"
          ]
        }
      ],
      "quarterSummary": {
        "totalBudget": "$320,000",
        "totalSavings": "$1,200,000",
        "netBenefit": "$880,000",
        "infrastructureRunRate": "$35,000/month",
        "keyMetrics": {}
      }
    }
  ]
}
```

**Required per Quarter:**
- `quarter`: Format `Q[1-4] YYYY`
- `theme`: Theme name
- `subtitle`: Focus area

**Objectives** can be:
- Simple strings
- Objects with detailed breakdown

### Metrics Groups
Named groups of related metrics (e.g., `costOptimization`, `agentExperience`, `platformCapabilities`, `financialKPIs`):

```json
{
  "costOptimization": {
    "title": "Cost Excellence",
    "metrics": [
      { "value": ">98%", "label": "Accuracy", "icon": "✅" }
    ]
  }
}
```

### Risk Mitigation
Risk management structure:
```json
{
  "riskMitigation": {
    "title": "Strategic Risk Management",
    "risks": [
      {
        "title": "Risk name",
        "mitigation": "Mitigation strategy",
        "costImpact": "Cost impact description",
        "monitoringKPI": "KPI to monitor"
      }
    ]
  }
}
```

---

## Validation

### Using the Validator

```bash
# Basic validation
python3 validate-roadmap.py -j my-roadmap.json

# Custom schema
python3 validate-roadmap.py -j my-roadmap.json -s custom-schema.json

# Check dependencies
python3 validate-roadmap.py --install-deps
```

### Validation Levels

1. **JSON Schema Validation** (if `jsonschema` installed)
   - Type checking
   - Required field validation
   - Pattern matching (URLs, colors, dates, quarters)
   - Value constraints (min/max length, format)

2. **Business Logic Validation** (always runs)
   - Navigation section references exist
   - No duplicate navigation IDs
   - Quarter format consistency
   - Proper section structure

### Exit Codes
- `0`: Success (all validations passed)
- `1`: Failure (schema or critical errors)

### Installation

```bash
# Install jsonschema for full validation
pip3 install jsonschema
```

Without `jsonschema`, the validator falls back to basic business logic checks only.

---

## Schema Extension Guidelines

To add new section types or properties:

1. **Add to schema**: Update `roadmap-schema.json`
   - Define structure in `definitions` if reusable
   - Add to section `patternProperties` if section-specific
   - Include description and constraints

2. **Update validator**: Add business logic checks in `validate-roadmap.py` if needed

3. **Document**: Update this file with examples

4. **Test**: Validate existing roadmaps against updated schema

---

## Common Patterns

### Currency Values
All currency values must use format: `$X,XXX` or `$X,XXX,XXX`
```json
"budget": "$285,000"
```

### Percentages
Percentage strings for targets/improvements:
```json
"roi": "158%",
"improvement": "71%"
```

### Quarters
Quarter identifiers must follow pattern `Q[1-4] YYYY`:
```json
"quarter": "Q2 2026"
```

### Hex Colors
All colors must be 6-digit hex codes:
```json
"color": "#ff6b6b",
"accentColor": "#F4454E"
```

### CSS Gradients
Theme gradients must be valid CSS:
```json
"primaryGradient": "linear-gradient(135deg, #08285E 0%, #436DB3 100%)"
```

---

## IDE Integration

### VS Code

Add to workspace `.vscode/settings.json`:
```json
{
  "json.schemas": [
    {
      "fileMatch": ["*roadmap*.json"],
      "url": "./Conversational-AI/Roadmap-Tool/roadmap-schema.json"
    }
  ]
}
```

This enables:
- Autocomplete for property names
- Inline validation errors
- Type checking
- Format hints

### JetBrains IDEs

1. Settings → Languages & Frameworks → Schemas and DTDs → JSON Schema Mappings
2. Add new mapping:
   - Name: "Stellarus Roadmap"
   - Schema file: `roadmap-schema.json`
   - File path pattern: `*roadmap*.json`

---

## Version History

### v1.0 (2026-05-07)
- Initial schema definition
- Support for customer and internal roadmap formats
- Comprehensive metadata, navigation, and sections
- Financial tracking and cost optimization
- Quarterly roadmap structures
- Metrics groups and risk mitigation

---

## Support

For schema questions or updates:
1. Validate your roadmap: `python3 validate-roadmap.py -j your-file.json`
2. Check error messages for specific violations
3. Reference this documentation for structure examples
4. Update schema for new patterns (with team review)

---

**Schema File**: `roadmap-schema.json`
**Validator**: `validate-roadmap.py`
**Last Updated**: 2026-05-07
