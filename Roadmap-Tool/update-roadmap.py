#!/usr/bin/env python3
"""
Roadmap Update Utility
Quick utility to add common elements to the roadmap data
"""

import json
import sys
from pathlib import Path

def load_roadmap_data(file_path="roadmap-data.json"):
    """Load the roadmap data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def save_roadmap_data(data, file_path="roadmap-data.json"):
    """Save the roadmap data to JSON file with pretty formatting"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved changes to {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving {file_path}: {e}")
        return False

def add_overview_metric(data):
    """Add a new metric to the overview section"""
    print("\n📊 Adding Overview Metric")
    
    icon = input("Enter emoji icon (e.g., 📈): ").strip()
    value = input("Enter metric value (e.g., 95%): ").strip()
    label = input("Enter metric label (e.g., Success Rate): ").strip()
    metric_type = input("Enter metric type (e.g., success-rate): ").strip() or "custom"
    
    if not all([icon, value, label]):
        print("❌ All fields are required")
        return False
    
    new_metric = {
        "type": metric_type,
        "value": value,
        "label": label,
        "icon": icon
    }
    
    data["sections"]["overview"]["metrics"].append(new_metric)
    print(f"✅ Added metric: {icon} {value} {label}")
    return True

def add_q2_feature(data):
    """Add a new feature to an existing Q2 card"""
    print("\n🎯 Adding Q2 Feature")
    
    # Show existing cards
    cards = data["sections"]["q2-details"]["cards"]
    print("Existing Q2 cards:")
    for i, card in enumerate(cards):
        print(f"  {i}: {card['title']}")
    
    try:
        card_index = int(input(f"Select card (0-{len(cards)-1}): "))
        if card_index < 0 or card_index >= len(cards):
            raise ValueError
    except ValueError:
        print("❌ Invalid card selection")
        return False
    
    feature_name = input("Enter feature name: ").strip()
    feature_description = input("Enter feature description: ").strip()
    
    if not all([feature_name, feature_description]):
        print("❌ Both name and description are required")
        return False
    
    new_feature = {
        "name": feature_name,
        "description": feature_description
    }
    
    cards[card_index]["features"].append(new_feature)
    print(f"✅ Added feature '{feature_name}' to card '{cards[card_index]['title']}'")
    return True

def add_quarter_objective(data):
    """Add an objective to a quarter"""
    print("\n🚀 Adding Quarter Objective")
    
    # Show existing quarters
    quarters = data["sections"]["q3-q1-roadmap"]["quarters"]
    print("Existing quarters:")
    for i, quarter in enumerate(quarters):
        print(f"  {i}: {quarter['quarter']} - {quarter['theme']}")
    
    try:
        quarter_index = int(input(f"Select quarter (0-{len(quarters)-1}): "))
        if quarter_index < 0 or quarter_index >= len(quarters):
            raise ValueError
    except ValueError:
        print("❌ Invalid quarter selection")
        return False
    
    objective = input("Enter new objective: ").strip()
    
    if not objective:
        print("❌ Objective cannot be empty")
        return False
    
    quarters[quarter_index]["objectives"].append(objective)
    print(f"✅ Added objective '{objective}' to {quarters[quarter_index]['quarter']}")
    return True

def add_success_metric(data):
    """Add a success metric"""
    print("\n📈 Adding Success Metric")
    
    # Choose category
    categories = ["costOptimization", "agentExperience"]
    print("Categories:")
    for i, cat in enumerate(categories):
        print(f"  {i}: {cat}")
    
    try:
        cat_index = int(input(f"Select category (0-{len(categories)-1}): "))
        category = categories[cat_index]
    except (ValueError, IndexError):
        print("❌ Invalid category selection")
        return False
    
    icon = input("Enter emoji icon: ").strip()
    label = input("Enter metric label: ").strip()
    value = input("Enter metric value: ").strip()
    detail = input("Enter detail text: ").strip()
    metric_type = input("Enter metric type: ").strip() or "custom"
    
    if not all([icon, label, value]):
        print("❌ Icon, label, and value are required")
        return False
    
    new_metric = {
        "type": metric_type,
        "label": label,
        "value": value,
        "detail": detail,
        "icon": icon
    }
    
    data["sections"]["metrics"][category]["metrics"].append(new_metric)
    print(f"✅ Added metric '{label}' to {category}")
    return True

def update_quarter_overview(data):
    """Update quarter overview focus information"""
    print("\n📅 Updating Quarter Overview")
    
    # Show existing quarter overview
    if "overview" not in data["sections"] or "quarterOverview" not in data["sections"]["overview"]:
        print("❌ No quarterOverview found in data")
        return False
        
    quarters = data["sections"]["overview"]["quarterOverview"]["quarters"]
    print("Existing quarters:")
    for i, quarter in enumerate(quarters):
        subheader = quarter.get("subheader", quarter.get("focus", "N/A"))  # Handle legacy format
        description = quarter.get("description", "")
        print(f"  {i}: {quarter['quarter']} - {subheader}")
        if description:
            print(f"     {description}")
    
    try:
        quarter_index = int(input(f"Select quarter to update (0-{len(quarters)-1}): "))
        if quarter_index < 0 or quarter_index >= len(quarters):
            raise ValueError
    except ValueError:
        print("❌ Invalid quarter selection")
        return False
    
    selected_quarter = quarters[quarter_index]
    print(f"\nUpdating {selected_quarter['quarter']}")
    
    # Get new values
    current_subheader = selected_quarter.get("subheader", selected_quarter.get("focus", ""))
    current_description = selected_quarter.get("description", "")
    
    new_subheader = input(f"Enter subheader (current: '{current_subheader}'): ").strip()
    new_description = input(f"Enter description (current: '{current_description}'): ").strip()
    
    # Update if provided
    if new_subheader:
        selected_quarter["subheader"] = new_subheader
        # Remove legacy 'focus' field if it exists
        if "focus" in selected_quarter:
            del selected_quarter["focus"]
    
    if new_description:
        selected_quarter["description"] = new_description
    
    print(f"✅ Updated {selected_quarter['quarter']} quarter overview")
    return True

def interactive_update(json_file="roadmap-data.json"):
    """Interactive update session"""
    print("🛠️ Roadmap Update Utility")
    print("=" * 40)
    print(f"📄 Working with: {json_file}")
    
    # Load data
    data = load_roadmap_data(json_file)
    if not data:
        return
    
    while True:
        print("\nOptions:")
        print("1. Add overview metric")
        print("2. Add Q2 feature")
        print("3. Add quarter objective")  
        print("4. Add success metric")
        print("5. Update quarter overview")
        print("6. Save and exit")
        print("7. Exit without saving")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            add_overview_metric(data)
        elif choice == "2":
            add_q2_feature(data)
        elif choice == "3":
            add_quarter_objective(data)
        elif choice == "4":
            add_success_metric(data)
        elif choice == "5":
            update_quarter_overview(data)
        elif choice == "6":
            if save_roadmap_data(data, json_file):
                print("✅ Changes saved successfully!")
                break
        elif choice == "7":
            print("👋 Exiting without saving")
            break
        else:
            print("❌ Invalid option")

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Interactive utility to update roadmap data',
        epilog='Example: python3 update-roadmap.py -j my-roadmap.json'
    )
    
    parser.add_argument(
        '-j', '--json',
        default='roadmap-data.json',
        help='JSON data filename to update (default: roadmap-data.json)'
    )
    
    args = parser.parse_args()
    
    interactive_update(args.json)

if __name__ == "__main__":
    main()