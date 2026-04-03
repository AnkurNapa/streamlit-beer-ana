#!/bin/bash

# Master Brewer Complete Setup Script
# Installs all dependencies and prepares the app

echo "🍺 Master Brewer - Complete Setup"
echo "=================================="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

echo "✅ Activating virtual environment..."
source .venv/bin/activate

echo "📥 Installing dependencies..."
uv pip install streamlit plotly pandas numpy firecrawl-py python-dotenv

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📖 Next Steps:"
echo "1. Get your Firecrawl API key from: https://www.firecrawl.dev/"
echo "2. Set environment variable:"
echo "   export FIRECRAWL_API_KEY='your_api_key_here'"
echo ""
echo "3. Scrape all Beer Analytics data:"
echo "   python scraper_enhanced.py"
echo ""
echo "4. Run the app:"
echo "   streamlit run app_comprehensive.py"
echo ""
echo "📚 Documentation:"
echo "   - README_COMPREHENSIVE.md - Full documentation"
echo "   - QUICK_START.md - Quick start guide"
echo "   - FIRECRAWL_SETUP.md - Detailed setup"
echo ""
echo "🎉 You're ready to brew!"
