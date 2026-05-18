#!/usr/bin/env python3
"""
Roadmap Data Validator
Validates roadmap JSON documents against the official JSON Schema
"""

import json
import sys
from pathlib import Path

# Try to import jsonschema (gracefully handle if not installed)
try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("⚠️  Warning: jsonschema library not installed. Install with: pip3 install jsonschema")
    print("   Falling back to basic validation.\n")

def load_schema(schema_path):
    """Load the JSON Schema from file"""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Schema file not found: {schema_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Schema JSON Parse Error: {e}")
        return None

def validate_with_schema(data, schema):
    """Validate data against JSON Schema"""
    try:
        validate(instance=data, schema=schema)
        return True, []
    except ValidationError as e:
        # Extract path to the error
        path = ".".join(str(p) for p in e.path) if e.path else "root"
        error_msg = f"{path}: {e.message}"
        return False, [error_msg]
    except SchemaError as e:
        return False, [f"Schema error: {e.message}"]

def validate_roadmap_data(file_path, schema_path="roadmap-schema.json"):
    """Main validation function"""
    print(f"🔍 Validating roadmap data: {file_path}")
    
    # Check file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File {file_path} not found")
        return False
    
    # Load and parse JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ File Error: {e}")
        return False
    
    # Load schema
    schema_file = Path(__file__).parent / schema_path
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        print("   Make sure roadmap-schema.json is in the same directory as this script.")
        return False
    
    schema = load_schema(schema_file)
    if schema is None:
        return False
    
    # Validate against schema if jsonschema is available
    if JSONSCHEMA_AVAILABLE:
        print("✓ Using JSON Schema validation")
        is_valid, errors = validate_with_schema(data, schema)
        
        if not is_valid:
            print("❌ Schema validation failed:")
            for error in errors:
                print(f"   • {error}")
            return False
        
        print("✅ Schema validation passed!")
    else:
        print("⚠️  Skipping schema validation (jsonschema not installed)")
        print("   Install with: pip3 install jsonschema")
    
    # Additional business logic validations
    errors = []
    
    # Check navigation references valid sections
    if "navigation" in data and "sections" in data:
        nav_sections = {item.get("section") for item in data["navigation"] if "section" in item}
        actual_sections = set(data["sections"].keys())
        invalid_refs = nav_sections - actual_sections
        
        if invalid_refs:
            errors.append(f"Navigation references non-existent sections: {', '.join(invalid_refs)}")
    
    # Check for duplicate navigation IDs
    if "navigation" in data:
        nav_ids = [item.get("id") for item in data["navigation"] if "id" in item]
        if len(nav_ids) != len(set(nav_ids)):
            errors.append("Duplicate navigation IDs detected")
    
    # Validate quarter format consistency
    if "sections" in data:
        for section_name, section_data in data["sections"].items():
            if isinstance(section_data, dict):
                # Check quarterOverview quarters
                if "quarterOverview" in section_data:
                    qo = section_data["quarterOverview"]
                    if "quarters" in qo and isinstance(qo["quarters"], list):
                        for i, q in enumerate(qo["quarters"]):
                            if "quarter" in q and not q["quarter"].startswith("Q"):
                                errors.append(f"sections.{section_name}.quarterOverview.quarters[{i}].quarter has invalid format: {q['quarter']}")
                
                # Check quarters array
                if "quarters" in section_data and isinstance(section_data["quarters"], list):
                    for i, q in enumerate(section_data["quarters"]):
                        if isinstance(q, dict) and "quarter" in q and not q["quarter"].startswith("Q"):
                            errors.append(f"sections.{section_name}.quarters[{i}].quarter has invalid format: {q['quarter']}")
    
    # Report business logic validation results
    if errors:
        print("\n⚠️  Business logic warnings:")
        for error in errors:
            print(f"   • {error}")
    
    # Generate summary
    nav_count = len(data.get("navigation", []))
    sections_count = len(data.get("sections", {}))
    
    # Count features across sections
    total_cards = 0
    total_features = 0
    for section_name, section_data in data.get("sections", {}).items():
        if isinstance(section_data, dict) and "cards" in section_data:
            cards = section_data["cards"]
            total_cards += len(cards)
            for card in cards:
                if "features" in card:
                    total_features += len(card["features"])
    
    print(f"\n📊 Roadmap Summary:")
    print(f"   • Title: {data.get('metadata', {}).get('pageTitle', 'N/A')}")
    print(f"   • Version: {data.get('metadata', {}).get('version', 'N/A')}")
    print(f"   • Last Updated: {data.get('metadata', {}).get('lastUpdated', 'N/A')}")
    print(f"   • Navigation items: {nav_count}")
    print(f"   • Sections: {sections_count}")
    print(f"   • Feature cards: {total_cards}")
    print(f"   • Total features: {total_features}")
    
    if errors:
        print(f"\n⚠️  Validation completed with {len(errors)} warning(s)")
        return True  # Still return True if only business logic warnings
    else:
        print("\n✅ All validations passed!")
        return True

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate roadmap JSON data against the official JSON Schema',
        epilog='Example: python3 validate-roadmap.py -j minerva-roadmap.json'
    )
    
    parser.add_argument(
        '-j', '--json',
        default='roadmap-data.json',
        help='JSON data filename to validate (default: roadmap-data.json)'
    )
    
    parser.add_argument(
        '-s', '--schema',
        default='roadmap-schema.json',
        help='JSON Schema filename (default: roadmap-schema.json)'
    )
    
    parser.add_argument(
        '--install-deps',
        action='store_true',
        help='Show command to install required dependencies'
    )
    
    args = parser.parse_args()
    
    if args.install_deps:
        print("To install required dependencies, run:")
        print("  pip3 install jsonschema")
        sys.exit(0)
    
    # Use provided JSON file or default
    json_file = args.json
    schema_file = args.schema
    
    # Validate
    success = validate_roadmap_data(json_file, schema_file)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
