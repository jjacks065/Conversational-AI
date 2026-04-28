#!/usr/bin/env python3
"""
Roadmap Generator - Create Self-Contained HTML Roadmaps
Generates a presentation-ready HTML file with embedded JSON data
"""

import json
import sys
import re
from pathlib import Path
import argparse

def sanitize_filename(title):
    """Convert title to filename-safe format"""
    # Replace spaces with dashes, remove special characters
    filename = re.sub(r'[^\w\s-]', '', title.strip())
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-').lower()

def find_json_file(directory, json_filename=None):
    """Find JSON data file in directory"""
    # If specific filename provided, use it
    if json_filename:
        json_path = Path(directory) / json_filename
        if json_path.exists():
            return json_path
        else:
            return None
    
    # Otherwise look for roadmap-data.json first
    roadmap_data = Path(directory) / 'roadmap-data.json'
    if roadmap_data.exists():
        return roadmap_data
    
    # Fall back to first JSON file found
    json_files = list(Path(directory).glob('*.json'))
    if json_files:
        return json_files[0]
    
    return None

def load_template(template_path):
    """Load the HTML template"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        return None

def load_roadmap_data(json_path):
    """Load roadmap data from JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON data: {e}")
        return None

def embed_data_in_template(template_html, roadmap_data):
    """Replace template loading logic with embedded data"""
    
    # Convert JSON to JavaScript object string
    js_data = json.dumps(roadmap_data, indent=8, ensure_ascii=False)
    
    # Create the replacement JavaScript code
    new_script = f"""    <script>
        let roadmapData = {js_data};
        let currentSection = 0;

        // Initialize template with embedded data
        function loadRoadmapData() {{
            console.log('✅ Using embedded roadmap data');
            initializeTemplate();
        }}

        function showError(message) {{
            document.body.innerHTML = `
                <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column; color: white;">
                    <h2>⚠️ Error Loading Roadmap</h2>
                    <p>${{message}}</p>
                </div>
            `;
        }}"""
    
    # Find and replace the script section
    script_pattern = r'<script>\s*let roadmapData = \{\};.*?function showError\(message\) \{.*?\}.*?\}'
    
    # Use a more specific pattern to find the exact section to replace
    start_pattern = r'<script>\s*let roadmapData = \{\};.*?let currentSection = 0;'
    end_pattern = r'function showError\(message\) \{[^}]*\}[^}]*\}'
    
    # Find the start and end positions
    start_match = re.search(start_pattern, template_html, re.DOTALL)
    end_match = re.search(end_pattern, template_html, re.DOTALL)
    
    if start_match and end_match:
        # Replace the section between start and end
        before = template_html[:start_match.start()]
        after = template_html[end_match.end():]
        result = before + new_script + after
        return result
    else:
        print("⚠️  Warning: Could not find exact script pattern. Using fallback replacement.")
        
        # Fallback: replace the entire script tag content
        script_tag_pattern = r'<script>.*?</script>'
        script_match = re.search(script_tag_pattern, template_html, re.DOTALL)
        
        if script_match:
            # Keep the functions after showError
            remaining_functions = extract_remaining_functions(template_html)
            full_script = new_script + "\n\n" + remaining_functions + "\n    </script>"
            
            result = template_html[:script_match.start()] + full_script + template_html[script_match.end():]
            return result
        else:
            print("❌ Error: Could not find script tag in template")
            return None

def extract_remaining_functions(template_html):
    """Extract the template functions that come after showError"""
    script_match = re.search(r'<script>(.*?)</script>', template_html, re.DOTALL)
    if not script_match:
        return ""
    
    script_content = script_match.group(1)
    
    # Find everything after showError function
    show_error_end = script_content.find('        }', script_content.find('function showError'))
    if show_error_end == -1:
        return ""
    
    # Find the actual end of showError function (could be multiple closing braces)
    remaining_content = script_content[show_error_end + 9:]  # Skip the closing brace and newline
    
    # Extract all the template functions
    functions = [
        'initializeTemplate',
        'buildNavigation', 
        'populateOverviewSection',
        'populateQ2Section',
        'populateRoadmapSection', 
        'populateMetricsSection',
        'showSection'
    ]
    
    function_code = ""
    for func_name in functions:
        func_pattern = f'function {func_name}\\(.*?\\{{[^{{}}]*(?:\\{{[^{{}}]*\\}}[^{{}}]*)*\\}}'
        func_match = re.search(func_pattern, remaining_content, re.DOTALL)
        if func_match:
            function_code += "        " + func_match.group(0) + "\n\n"
    
    # Add the DOMContentLoaded listener
    dom_pattern = r'document\.addEventListener\(\'DOMContentLoaded\', loadRoadmapData\);'
    dom_match = re.search(dom_pattern, remaining_content)
    if dom_match:
        function_code += "        " + dom_match.group(0)
    
    return function_code.rstrip()

def generate_roadmap(working_dir, template_path=None, output_name=None, json_filename=None):
    """Generate roadmap HTML from JSON data"""
    
    working_path = Path(working_dir)
    if not working_path.exists():
        print(f"❌ Working directory does not exist: {working_dir}")
        return False
    
    print(f"🔍 Scanning directory: {working_path.absolute()}")
    
    # Find JSON file
    json_file = find_json_file(working_path, json_filename)
    if not json_file:
        if json_filename:
            print(f"❌ JSON file '{json_filename}' not found in {working_dir}")
        else:
            print(f"❌ No JSON file found in {working_dir}")
        return False
    
    print(f"📄 Found JSON data: {json_file.name}")
    
    # Load roadmap data
    roadmap_data = load_roadmap_data(json_file)
    if not roadmap_data:
        return False
    
    # Determine template path
    if not template_path:
        # Look for template in the same directory as this script
        script_dir = Path(__file__).parent
        template_path = script_dir / "Roadmap-Template.html"
    
    template_path = Path(template_path)
    if not template_path.exists():
        print(f"❌ Template file not found: {template_path}")
        return False
    
    print(f"📋 Using template: {template_path.name}")
    
    # Load template
    template_html = load_template(template_path)
    if not template_html:
        return False
    
    # Embed data in template
    result_html = embed_data_in_template(template_html, roadmap_data)
    if not result_html:
        return False
    
    # Generate output filename
    if not output_name:
        title = roadmap_data.get('metadata', {}).get('title', 'roadmap')
        output_name = sanitize_filename(title) + '.html'
    
    output_path = working_path / output_name
    
    # Write output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result_html)
        
        print(f"✅ Generated roadmap: {output_path.name}")
        print(f"📍 File location: {output_path.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        return False

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description='Generate self-contained HTML roadmap from JSON data',
        epilog='Example: python3 generate-roadmap.py /path/to/data'
    )
    
    parser.add_argument(
        'working_dir',
        help='Directory containing JSON data file'
    )
    
    parser.add_argument(
        '-t', '--template',
        help='Path to HTML template file (default: Roadmap-Template.html in script directory)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output filename (default: generated from JSON metadata title)'
    )
    
    parser.add_argument(
        '-j', '--json',
        help='JSON data filename (default: roadmap-data.json)'
    )
    
    parser.add_argument(
        '--list-json',
        action='store_true',
        help='List JSON files in working directory and exit'
    )
    
    args = parser.parse_args()
    
    if args.list_json:
        working_path = Path(args.working_dir)
        json_files = list(working_path.glob('*.json'))
        if json_files:
            print(f"JSON files in {working_path}:")
            for json_file in json_files:
                print(f"  • {json_file.name}")
        else:
            print(f"No JSON files found in {working_path}")
        return
    
    print("🚀 Roadmap Generator")
    print("=" * 50)
    
    success = generate_roadmap(
        working_dir=args.working_dir,
        template_path=args.template,
        output_name=args.output,
        json_filename=args.json
    )
    
    if success:
        print("\n🎉 Roadmap generation complete!")
        print("   Open the generated HTML file in any browser - no server required!")
    else:
        print("\n❌ Roadmap generation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()