# Roadmap Schema Quick Reference

## 📊 Visual Structure Overview

```
roadmap.json
├── metadata (required)
│   ├── title (required)
│   ├── pageTitle (required)
│   ├── logoPath (optional)
│   ├── disclaimer (required)
│   ├── theme (required)
│   │   ├── primaryGradient (required)
│   │   ├── accentColor (required)
│   │   ├── costColor (optional)
│   │   └── warningColor (optional)
│   ├── version (optional)
│   └── lastUpdated (optional)
│
├── navigation (required, array)
│   └── [navigation item]
│       ├── id (required, integer ≥ 0)
│       ├── label (required, string)
│       └── section (required, string, must exist in sections)
│
└── sections (required, object)
    └── [section-id] (dynamic keys)
        ├── title (required)
        ├── metrics (optional, array of metric objects)
        ├── transformation (optional)
        │   ├── title (required)
        │   └── description (required)
        ├── quarterOverview (optional)
        │   ├── title (required)
        │   └── quarters (required, array)
        │       └── [quarter]
        │           ├── quarter (required, "Q# YYYY")
        │           ├── subheader (required)
        │           ├── description (required)
        │           ├── budget (optional)
        │           ├── costPerRequest (optional)
        │           ├── projectedSavings (optional)
        │           └── roi (optional)
        ├── financialSummary (optional)
        │   ├── title (required)
        │   ├── totalInvestment (optional)
        │   ├── projectedSavings (optional)
        │   ├── netBenefit (optional)
        │   ├── paybackPeriod (optional)
        │   └── breakdown (optional, array)
        ├── cards (optional, array for Q2 details)
        │   └── [card]
        │       ├── title (required)
        │       ├── color (required, #RRGGBB)
        │       ├── target (optional)
        │       ├── scope (optional)
        │       ├── budget (optional)
        │       ├── costMetrics (optional)
        │       ├── costBenefit (optional)
        │       └── features (required, array)
        │           └── [feature]
        │               ├── name (required)
        │               ├── description (required)
        │               ├── costDrivers (optional)
        │               └── costSavings (optional)
        ├── quarters (optional, array for Q3-Q1 roadmap)
        │   └── [quarter]
        │       ├── quarter (required, "Q# YYYY")
        │       ├── theme (required)
        │       ├── subtitle (required)
        │       ├── budget (optional)
        │       ├── costPerRequest (optional)
        │       ├── projectedSavings (optional)
        │       ├── roi (optional)
        │       ├── objectives (optional, array of strings or objects)
        │       └── quarterSummary (optional)
        ├── costOptimization (optional, metrics group)
        │   ├── title (required)
        │   └── metrics (required, array)
        ├── agentExperience (optional, metrics group)
        ├── platformCapabilities (optional, metrics group)
        ├── financialKPIs (optional, metrics group)
        └── riskMitigation (optional)
            ├── title (required)
            └── risks (required, array)
                └── [risk]
                    ├── title (required)
                    ├── mitigation (required)
                    ├── costImpact (optional)
                    └── monitoringKPI (optional)
```

---

## 🎯 Metric Object Structure

```
metric
├── type (optional, string)
├── value (required, string)
├── label (required, string, 1-100 chars)
├── icon (required, string, 1-10 chars, typically emoji)
├── detail (optional, string)
├── costImpact (optional, string)
├── costImplication (optional, string, alias for costImpact)
├── baseline (optional, string)
├── q2Target (optional, string)
├── q3Target (optional, string)
├── q4Target (optional, string)
├── q1'27Target (optional, string)
├── improvement (optional, string)
├── q2 (optional, string)
├── q3 (optional, string)
├── q4 (optional, string)
├── q1'27 (optional, string)
├── annual (optional, string)
├── optimization (optional, string)
├── q2End (optional, string)
├── q3End (optional, string)
├── q4End (optional, string)
├── q1'27End (optional, string)
├── paybackMonth (optional, string)
└── q1Baseline (optional, string)
```

---

## 📋 Common Section Patterns

### Overview Section
```json
{
  "sections": {
    "overview": {
      "title": "Strategic Overview",
      "metrics": [/* array of metric objects */],
      "transformation": {
        "title": "...",
        "description": "..."
      },
      "quarterOverview": {
        "title": "Year Overview",
        "quarters": [/* array of quarter summaries */]
      },
      "financialSummary": {/* optional financial data */}
    }
  }
}
```

### Q2 Details Section
```json
{
  "sections": {
    "q2-details": {
      "title": "Q2 2026: Detailed Implementation",
      "quarterBudget": "$285,000",
      "costBreakdown": {/* category breakdown */},
      "cards": [/* array of feature cards */],
      "quarterSummary": {/* summary metrics */}
    }
  }
}
```

### Q3-Q1 Roadmap Section
```json
{
  "sections": {
    "q3-q1-roadmap": {
      "title": "Q3 2026 - Q1 2027: Platform Excellence",
      "quarters": [
        {
          "quarter": "Q3 2026",
          "theme": "Growth & Scale",
          "subtitle": "...",
          "budget": "$320,000",
          "objectives": [/* strings or detailed objects */],
          "quarterSummary": {/* summary */}
        }
      ]
    }
  }
}
```

### Metrics Section
```json
{
  "sections": {
    "metrics": {
      "title": "Success Metrics",
      "costOptimization": {
        "title": "Cost Excellence",
        "metrics": [/* metric objects */]
      },
      "agentExperience": {
        "title": "Agent Experience",
        "metrics": [/* metric objects */]
      },
      "platformCapabilities": {/* ... */},
      "financialKPIs": {/* ... */},
      "riskMitigation": {
        "title": "Risk Management",
        "risks": [/* risk objects */]
      }
    }
  }
}
```

---

## 🔑 Key Patterns & Constraints

### Required at Root Level
- ✅ `metadata` (object)
- ✅ `navigation` (array, at least 1 item)
- ✅ `sections` (object, at least 1 section)

### Metadata Theme Required
- ✅ `primaryGradient` (CSS gradient string)
- ✅ `accentColor` (hex color #RRGGBB)

### Navigation Items Required
- ✅ `id` (unique integer ≥ 0)
- ✅ `label` (string, 1-50 chars)
- ✅ `section` (string, must match a section key)

### Every Section Required
- ✅ `title` (string, 1-200 chars)

### Every Metric Required
- ✅ `value` (string)
- ✅ `label` (string, 1-100 chars)
- ✅ `icon` (string, 1-10 chars)

### Every Card Required
- ✅ `title` (string)
- ✅ `color` (hex color #RRGGBB)
- ✅ `features` (array, at least 1 feature)

### Every Feature Required
- ✅ `name` (string)
- ✅ `description` (string)

### Quarter Format
- ✅ Must match pattern: `Q[1-4] YYYY` (e.g., "Q2 2026")

### Currency Format
- ✅ Must match pattern: `$X,XXX` or `$X,XXX,XXX`

### Date Format
- ✅ Must match pattern: `YYYY-MM-DD` (e.g., "2026-05-07")

### Version Format
- ✅ Must match pattern: `X.Y` or `X.Y-Suffix` (e.g., "2.0-Internal")

---

## ⚡ Quick Validation Checklist

Before generating your roadmap, verify:

- [ ] All required root properties present (`metadata`, `navigation`, `sections`)
- [ ] Theme has both `primaryGradient` and `accentColor`
- [ ] All navigation items have unique IDs
- [ ] All navigation `section` values exist in `sections` object
- [ ] All sections have a `title`
- [ ] All metrics have `value`, `label`, and `icon`
- [ ] All cards have `title`, `color`, and at least one `feature`
- [ ] All features have `name` and `description`
- [ ] All quarter strings match format `Q[1-4] YYYY`
- [ ] All currency values match pattern `$X,XXX`
- [ ] All hex colors are 6 digits (no 3-digit shorthand)
- [ ] CSS gradients start with `linear-gradient` or `radial-gradient`

---

## 🚀 Validation Command

```bash
# Quick validation
python3 validate-roadmap.py -j your-roadmap.json

# Expected output if valid:
# ✓ Using JSON Schema validation
# ✅ Schema validation passed!
# 📊 Roadmap Summary: ...
# ✅ All validations passed!
```

---

## 📚 For More Details

- **Full Schema**: See `roadmap-schema.json`
- **Complete Documentation**: See `SCHEMA-DOCUMENTATION.md`
- **Project Overview**: See `SCHEMA-PROJECT-SUMMARY.md`
- **Main README**: See `README.md`

---

**Last Updated**: 2026-05-07
**Schema Version**: 1.0
