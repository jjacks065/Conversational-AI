#!/usr/bin/env python3
"""
Roadmap Data Validator
Validates the roadmap-data.json file structure and required fields
"""

import json
import sys
from pathlib import Path

def validate_required_fields(data, required_fields, path=""):
    """Validate that all required fields exist in the data structure"""
    errors = []
    
    for field in required_fields:
        if isinstance(field, dict):
            # Nested field validation
            for parent_field, child_fields in field.items():
                if parent_field not in data:
                    errors.append(f"Missing required field: {path}.{parent_field}")
                elif isinstance(child_fields, list):
                    errors.extend(validate_required_fields(
                        data[parent_field], 
                        child_fields, 
                        f"{path}.{parent_field}" if path else parent_field
                    ))
        else:
            # Simple field validation
            if field not in data:
                errors.append(f"Missing required field: {path}.{field}" if path else f"Missing required field: {field}")
    
    return errors

def validate_roadmap_data(file_path):
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
    
    # Define required structure
    required_structure = [
        {
            "metadata": [
                "title", "pageTitle", "disclaimer", 
                {"theme": ["primaryGradient", "accentColor"]}
            ]
        },
        "navigation",
        {
            "sections": [
                {
                    "overview": [
                        "title", "metrics", "transformation", "quarterOverview"
                    ]
                },
                {
                    "q2-details": [
                        "title", "cards"
                    ]
                },
                {
                    "q3-q1-roadmap": [
                        "title", "quarters"
                    ]
                },
                {
                    "metrics": [
                        "title"
                    ]
                }
            ]
        }
    ]
    
    # Validate structure
    errors = validate_required_fields(data, required_structure)
    
    # Additional validations
    
    # Check navigation items have required fields
    if "navigation" in data and isinstance(data["navigation"], list):
        for i, nav_item in enumerate(data["navigation"]):
            nav_errors = validate_required_fields(nav_item, ["id", "label", "section"], f"navigation[{i}]")
            errors.extend(nav_errors)
    
    # Check metrics have icons and values in any section that has metrics
    if "sections" in data:
        for section_name, section_data in data["sections"].items():
            if isinstance(section_data, dict):
                # Check direct metrics array (like in overview)
                if "metrics" in section_data and isinstance(section_data["metrics"], list):
                    for i, metric in enumerate(section_data["metrics"]):
                        metric_errors = validate_required_fields(
                            metric, 
                            ["value", "label", "icon"], 
                            f"sections.{section_name}.metrics[{i}]"
                        )
                        errors.extend(metric_errors)
                
                # Check nested metrics structures (like costOptimization, performanceExcellence, etc.)
                for key, value in section_data.items():
                    if isinstance(value, dict) and "metrics" in value and isinstance(value["metrics"], list):
                        for i, metric in enumerate(value["metrics"]):
                            metric_errors = validate_required_fields(
                                metric, 
                                ["value", "label", "icon"], 
                                f"sections.{section_name}.{key}.metrics[{i}]"
                            )
                            errors.extend(metric_errors)
    
    # Check Q2 cards have required structure
    if "q2-details" in data.get("sections", {}):
        q2_section = data["sections"]["q2-details"]
        if "cards" in q2_section:
            for i, card in enumerate(q2_section["cards"]):
                card_errors = validate_required_fields(
                    card,
                    ["title", "color", "features"],
                    f"sections.q2-details.cards[{i}]"
                )
                errors.extend(card_errors)
                
                # Validate features
                if "features" in card:
                    for j, feature in enumerate(card["features"]):
                        feature_errors = validate_required_fields(
                            feature,
                            ["name", "description"],
                            f"sections.q2-details.cards[{i}].features[{j}]"
                        )
                        errors.extend(feature_errors)
    
    # Check quarterOverview quarters have required structure
    if "overview" in data.get("sections", {}):
        overview_section = data["sections"]["overview"]
        if "quarterOverview" in overview_section and "quarters" in overview_section["quarterOverview"]:
            quarters = overview_section["quarterOverview"]["quarters"]
            for i, quarter in enumerate(quarters):
                quarter_errors = validate_required_fields(
                    quarter,
                    ["quarter", "subheader", "description"],
                    f"sections.overview.quarterOverview.quarters[{i}]"
                )
                errors.extend(quarter_errors)
    
    # Report results
    if errors:
        print("❌ Validation failed with the following errors:")
        for error in errors:
            print(f"   • {error}")
        return False
    else:
        print("✅ Validation passed! Roadmap data structure is valid.")
        
        # Additional info
        nav_count = len(data.get("navigation", []))
        sections_count = len(data.get("sections", {}))
        q2_cards = len(data.get("sections", {}).get("q2-details", {}).get("cards", []))
        
        print(f"📊 Data Summary:")
        print(f"   • Navigation items: {nav_count}")
        print(f"   • Sections: {sections_count}")
        print(f"   • Q2 feature cards: {q2_cards}")
        
        return True

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate roadmap JSON data structure and required fields',
        epilog='Example: python3 validate-roadmap.py -j my-roadmap.json'
    )
    
    parser.add_argument(
        '-j', '--json',
        default='roadmap-data.json',
        help='JSON data filename to validate (default: roadmap-data.json)'
    )
    
    # Support legacy positional argument for backwards compatibility
    parser.add_argument(
        'file_path',
        nargs='?',
        help='JSON file path (legacy - use --json instead)'
    )
    
    args = parser.parse_args()
    
    # Use positional argument if provided (legacy), otherwise use --json option
    file_path = args.file_path if args.file_path else args.json
    
    success = validate_roadmap_data(file_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()