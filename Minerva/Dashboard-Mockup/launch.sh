#!/bin/bash

# Stellarus Minerva Dashboard Launcher
# Quick script to launch the dashboard mockup

echo "🌟 Starting Stellarus Minerva Performance Dashboard..."
echo "📊 Dashboard Mockup - Brand Guidelines Compliant"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✅ Python3 found - Starting HTTP server on port 8080"
    echo "🌐 Open: http://localhost:8080"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo "----------------------------------------"
    python3 -m http.server 8080
elif command -v python &> /dev/null; then
    echo "✅ Python found - Starting HTTP server on port 8080"
    echo "🌐 Open: http://localhost:8080"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo "----------------------------------------"
    python -m http.server 8080
else
    echo "⚠️  Python not found. Please install Python or open index.html directly in your browser."
    echo ""
    echo "Alternative launch methods:"
    echo "1. Open index.html directly in your browser"
    echo "2. Use 'npx serve .' if Node.js is installed"
    echo "3. Use any local web server of your choice"
fi