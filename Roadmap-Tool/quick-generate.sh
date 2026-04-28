#!/bin/bash
# Quick Roadmap Generator
# Usage: ./quick-generate.sh [directory]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKING_DIR="${1:-.}"

echo "🚀 Quick Roadmap Generator"
echo "=========================="

if [ ! -d "$WORKING_DIR" ]; then
    echo "❌ Directory '$WORKING_DIR' does not exist"
    exit 1
fi

echo "📂 Working directory: $WORKING_DIR"
echo "🔧 Generating roadmap..."

cd "$SCRIPT_DIR"
python3 generate-roadmap.py "$WORKING_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo "✨ Success! Your roadmap is ready to present."
    echo "💡 Tip: Double-click the generated HTML file to open it in your browser"
    
    # Ask if user wants to open the file
    read -p "🤔 Open the roadmap now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Find the generated HTML file
        GENERATED_FILE=$(find "$WORKING_DIR" -name "*.html" -not -name "*Template*" | head -n 1)
        if [ -n "$GENERATED_FILE" ]; then
            echo "🌐 Opening $GENERATED_FILE"
            open "$GENERATED_FILE" 2>/dev/null || xdg-open "$GENERATED_FILE" 2>/dev/null || echo "Please open $GENERATED_FILE manually"
        fi
    fi
else
    echo ""
    echo "❌ Generation failed. Check the error messages above."
    exit 1
fi