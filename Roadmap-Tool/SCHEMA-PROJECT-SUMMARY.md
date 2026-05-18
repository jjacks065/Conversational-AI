# Roadmap Tool - Schema Contract & Validation

## 🎯 Project Status

**Completed**: JSON Schema contract and validation system for the Roadmap-Tool

### What Was Built

1. **JSON Schema Contract** (`roadmap-schema.json`)
   - Comprehensive JSON Schema (Draft-07) defining the structure for all roadmap documents
   - Enforces required fields, data types, patterns, and constraints
   - Supports both customer-facing and internal roadmaps
   - Extensible design for future roadmap formats

2. **Schema-Based Validator** (`validate-roadmap.py`)
   - Upgraded from basic field checking to full JSON Schema validation
   - Two-tier validation: Schema validation + Business logic validation
   - Graceful degradation (works without jsonschema library)
   - Enhanced reporting with detailed summaries

3. **Documentation** (`SCHEMA-DOCUMENTATION.md`)
   - Complete schema reference guide
   - Property-by-property documentation with examples
   - Validation instructions
   - IDE integration guidance
   - Extension guidelines for future enhancements

---

## 📋 Schema Overview

### Top-Level Structure
```json
{
  "metadata": { ... },    // Required: Presentation configuration
  "navigation": [ ... ],  // Required: Navigation menu
  "sections": { ... }     // Required: Content sections
}
```

### Key Features

**Validation Coverage:**
- ✅ Required field enforcement
- ✅ Type checking (string, integer, object, array)
- ✅ Pattern matching (hex colors, currency, dates, quarters)
- ✅ Value constraints (min/max length, ranges)
- ✅ Custom business logic (navigation references, duplicate IDs)

**Supported Structures:**
- Metadata with theming and versioning
- Dynamic navigation with section linking
- Flexible section definitions
- Metrics (direct and grouped)
- Financial summaries and cost breakdowns
- Feature cards with cost analysis
- Quarterly roadmaps with objectives
- Risk mitigation strategies

---

## 🚀 Usage

### Validate a Roadmap

```bash
# Basic validation
python3 validate-roadmap.py -j roadmap-data.json

# With custom schema
python3 validate-roadmap.py -j my-roadmap.json -s custom-schema.json

# Check from different directory
python3 validate-roadmap.py -j ../Minerva/Roadmap/minerva-internal-roadmap-v2.json
```

### Example Output

```
🔍 Validating roadmap data: minerva-internal-roadmap-v2.json
✓ Using JSON Schema validation
✅ Schema validation passed!

📊 Roadmap Summary:
   • Title: 🚀 CSR Chat Internal Roadmap & Budget
   • Version: 2.0-Internal
   • Last Updated: 2026-05-06
   • Navigation items: 4
   • Sections: 4
   • Feature cards: 4
   • Total features: 14

✅ All validations passed!
```

### Install Dependencies (Optional)

For full JSON Schema validation:
```bash
pip3 install jsonschema
```

Without `jsonschema`, the validator falls back to basic validation with a warning.

---

## 📁 Files Created

### 1. `roadmap-schema.json` (900+ lines)
Comprehensive JSON Schema defining:
- Metadata structure with theme configuration
- Navigation array with section linking
- Dynamic sections with flexible properties
- 13+ reusable definitions (metric, card, quarterRoadmap, etc.)
- Pattern-based property validation
- Detailed constraints and descriptions

### 2. `validate-roadmap.py` (Updated, 220 lines)
Enhanced validator featuring:
- JSON Schema-based validation (when available)
- Business logic validation (always runs)
- Graceful library handling
- Detailed error reporting
- Comprehensive roadmap summary
- CLI with flags for JSON file and schema file

### 3. `SCHEMA-DOCUMENTATION.md` (500+ lines)
Complete documentation including:
- Schema overview and purpose
- Property-by-property reference
- Required vs optional fields
- Pattern specifications
- Usage examples
- Validation guide
- IDE integration instructions
- Extension guidelines

---

## 🎨 Schema Highlights

### Metadata Validation
```json
{
  "title": "String (1-200 chars)",
  "theme": {
    "primaryGradient": "Must be valid CSS gradient",
    "accentColor": "Must be #RRGGBB hex format"
  },
  "version": "Must match X.Y or X.Y-Suffix pattern",
  "lastUpdated": "Must be YYYY-MM-DD format"
}
```

### Navigation Validation
- IDs must be unique integers ≥ 0
- Section references must exist in `sections` object
- Labels must be 1-50 characters

### Metrics Validation
All metrics require:
- `value` (string)
- `label` (string, 1-100 chars)
- `icon` (string, 1-10 chars, typically emoji)

### Financial Fields
Currency values must match pattern: `$X,XXX` or `$X,XXX,XXX`

### Quarter Format
All quarter identifiers must match: `Q[1-4] YYYY` (e.g., "Q2 2026")

---

## 🔧 Validator Features

### Two-Tier Validation

**Tier 1: JSON Schema Validation** (if `jsonschema` installed)
- Structural validation
- Type enforcement
- Pattern matching
- Required field checking

**Tier 2: Business Logic Validation** (always runs)
- Navigation section references exist
- No duplicate navigation IDs
- Quarter format consistency
- Cross-section validation

### Exit Codes
- `0`: Success (all validations passed)
- `1`: Failure (errors detected)

### Error Reporting
- Clear error messages with paths (e.g., `sections.overview.metrics[2]: missing 'icon'`)
- Warnings for business logic issues
- Detailed summary of roadmap contents

---

## 🧪 Testing Results

### Validated Against
- `minerva-internal-roadmap-v2.json` ✅
  - 4 navigation items
  - 4 sections
  - 4 feature cards with 14 total features
  - Complex cost optimization structures
  - Quarterly financial breakdowns

### Validation Coverage
- ✅ All required fields present
- ✅ Proper data types
- ✅ Valid hex colors
- ✅ Correct quarter formats
- ✅ Currency pattern compliance
- ✅ Navigation section linking

---

## 📊 Schema Statistics

- **Total definitions**: 13 reusable schemas
- **Validated properties**: 60+ unique properties
- **Pattern validations**: 8 regex patterns
- **Nested depth**: Up to 5 levels deep
- **Flexibility**: Supports both simple and complex roadmaps

---

## 🔄 Integration Workflow

### For New Roadmaps

1. **Create JSON document** following schema structure
2. **Validate**: `python3 validate-roadmap.py -j new-roadmap.json`
3. **Fix errors** based on validation output
4. **Generate HTML**: `python3 generate-roadmap.py -j new-roadmap.json .`
5. **Present**: Open generated HTML in browser

### For Existing Roadmaps

1. **Validate**: `python3 validate-roadmap.py -j existing-roadmap.json`
2. **Review warnings** and fix if needed
3. **Regenerate** if changes were made

---

## 🎯 Benefits

### For Roadmap Authors
- **Clear structure**: Know exactly what fields are required
- **Immediate feedback**: Catch errors before generation
- **IDE support**: Autocomplete and inline validation
- **Consistency**: All roadmaps follow the same pattern

### For Stakeholders
- **Reliability**: Validated roadmaps always render correctly
- **Standards**: Consistent structure across all presentations
- **Quality**: Automated checks prevent missing information

### For Developers
- **Contract**: Single source of truth for roadmap structure
- **Extensibility**: Easy to add new properties/sections
- **Maintenance**: Schema documents the data model
- **Testing**: Automated validation in CI/CD pipelines

---

## 🚀 Future Enhancements

Potential additions (not implemented):

1. **Schema versioning**: Support multiple schema versions
2. **Custom validators**: Plugin system for domain-specific rules
3. **Auto-fix**: Suggest corrections for common errors
4. **Diff validation**: Compare roadmap versions
5. **Migration tools**: Upgrade old roadmaps to new schema versions
6. **Template generation**: Generate skeleton roadmaps from schema

---

## 📝 Usage Examples

### Customer Roadmap Validation
```bash
python3 validate-roadmap.py -j minerva-customer-roadmap-v2.json
```

### Internal Roadmap Validation
```bash
python3 validate-roadmap.py -j minerva-internal-roadmap-v2.json
```

### CI/CD Integration
```bash
# In your CI pipeline
python3 validate-roadmap.py -j roadmap.json || exit 1
python3 generate-roadmap.py -j roadmap.json .
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
if git diff --cached --name-only | grep -q 'roadmap.*\.json'; then
    python3 validate-roadmap.py -j roadmap-data.json || exit 1
fi
```

---

## 🎓 Key Learnings

1. **Schema as Contract**: JSON Schema provides both validation and documentation
2. **Graceful Degradation**: Tools should work even without optional dependencies
3. **Two-Tier Validation**: Schema for structure, custom logic for business rules
4. **Clear Errors**: Good error messages include paths and context
5. **IDE Integration**: Schema files enable developer productivity features

---

## 📚 References

- **JSON Schema**: [json-schema.org](https://json-schema.org/)
- **Draft-07 Spec**: [JSON Schema Draft-07](https://json-schema.org/draft-07/schema)
- **Python jsonschema**: [pypi.org/project/jsonschema](https://pypi.org/project/jsonschema/)

---

**Project**: Roadmap-Tool Schema Contract
**Status**: ✅ Complete
**Date**: 2026-05-07
**Files**: 3 created/updated
**Lines of Code**: 1,600+ (schema + validator + docs)
