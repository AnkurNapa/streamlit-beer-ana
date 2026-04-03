# 🍺 Master Brewer - Getting Started Guide

Complete implementation of all Beer Analytics features in Streamlit!

---

## ⚡ 3-Minute Quick Start

### Step 1: Get API Key (2 min)
```bash
# Visit: https://www.firecrawl.dev/
# Sign up → Copy API key
```

### Step 2: Set API Key
```bash
export FIRECRAWL_API_KEY="your_api_key_here"
```

### Step 3: Scrape Data
```bash
source .venv/bin/activate
python scraper_enhanced.py
```

### Step 4: Run App
```bash
streamlit run app_comprehensive.py
```

Done! Visit http://localhost:8501

---

## 📂 What Was Built

### **3 New Python Modules**

1. **`scraper_enhanced.py`** (Enhanced Scraper)
   - Scrapes ALL data from Beer Analytics
   - 500+ hops with detailed profiles
   - 100+ yeasts with characteristics
   - BJCP beer style guidelines
   - Grains/fermentables database
   - 1M+ community recipes
   - Saves to JSON for caching

2. **`data_loader_enhanced.py`** (Advanced Data Loader)
   - Load and manage all data
   - Advanced filtering (recipes, hops, yeasts, fermentables)
   - Search & recommendations
   - Style-based suggestions
   - Community statistics

3. **`app_comprehensive.py`** (Main App)
   - 15 pages with all features
   - Complete navigation
   - Advanced filtering dashboard
   - Analytics & visualizations
   - Recipe builder

### **6 Documentation Files**

- `README_COMPREHENSIVE.md` - Full feature list
- `GETTING_STARTED.md` - This file
- `QUICK_START.md` - Quick start (5 min)
- `FIRECRAWL_SETUP.md` - Detailed setup
- `SETUP_COMPLETE.sh` - Auto setup script

---

## 🎯 All Features Implemented

### **📚 Data & Exploration** (5 Pages)
- ✅ **Home** - Overview & quick stats
- ✅ **Recipe Search** - 1M+ recipes with filtering
- ✅ **Beer Styles** - BJCP guidelines
- ✅ **Hop Library** - 500+ hops with pairings
- ✅ **Yeast Library** - 100+ yeasts with profiles
- ✅ **Fermentables** - Grains & malts database

### **🔧 Tools & Calculators** (5 Pages)
- ✅ **Advanced Filters** - Multi-criteria filtering
- ✅ **Flavor Wheel** - Flavor comparisons
- ✅ **IBU/ABV/Color** - Calculators & charts
- ✅ **Hop Pairings** - Compatible hops
- ✅ **Recipe Builder** - Step-by-step creation

### **📊 Analytics** (3 Pages)
- ✅ **Community Statistics** - Overall stats & charts
- ✅ **Trending** - Popular items (top 10)
- ✅ **Popular Items** - Most used ingredients

---

## 🗂️ File Locations

```
📦 streamlit_beer_ana/
├── 🚀 app_comprehensive.py          ← MAIN APP
├── 🔄 scraper_enhanced.py          ← DATA SCRAPER
├── 📚 data_loader_enhanced.py      ← DATA LOADER
│
├── 📖 README_COMPREHENSIVE.md      ← FULL DOCS
├── ⚡ GETTING_STARTED.md           ← THIS FILE
├── 🏃 QUICK_START.md               ← 5-MIN GUIDE
├── 🔧 FIRECRAWL_SETUP.md           ← SETUP DETAILS
├── 📜 SETUP_COMPLETE.sh            ← AUTO SETUP
│
├── 📁 data/
│   └── beer-analytics-full/        ← SCRAPED DATA
│       ├── hops_detailed.json
│       ├── yeasts_detailed.json
│       ├── beer_styles_detailed.json
│       ├── fermentables_detailed.json
│       ├── recipes_advanced.json
│       └── search_options.json
│
└── 🐍 .venv/                       ← VIRTUAL ENV
```

---

## 🎮 Using the App

### **Sidebar Navigation**

The app has organized sections:

1. **🏠 Home** - Start here
2. **📚 Explore Data** - Search & learn
   - Recipe Search
   - Beer Styles
   - Hop Library
   - Yeast Library
   - Fermentables

3. **🔧 Tools & Calculators**
   - Advanced Filters
   - Flavor Wheel
   - IBU/ABV/Color
   - Hop Pairings

4. **📈 Analytics**
   - Community Stats
   - Trending
   - Popular Items

5. **🧪 Build**
   - Recipe Builder

### **Typical Workflow**

```
1. Start at Home (get overview)
   ↓
2. Search Recipes (find inspiration)
   ↓
3. Explore Beer Styles (understand guidelines)
   ↓
4. Check Hop Library (learn ingredients)
   ↓
5. Use Recipe Builder (create your own)
```

---

## 💻 Commands Reference

### Setup
```bash
# Auto setup (installs everything)
chmod +x SETUP_COMPLETE.sh
./SETUP_COMPLETE.sh
```

### Data Scraping
```bash
# Activate environment
source .venv/bin/activate

# Set API key
export FIRECRAWL_API_KEY="your_key"

# Scrape all data (takes 5-10 min)
python scraper_enhanced.py

# Data saved to: data/beer-analytics-full/
```

### Running App
```bash
# Activate environment
source .venv/bin/activate

# Run comprehensive app
streamlit run app_comprehensive.py

# App opens at: http://localhost:8501
```

### Optional: Original App
```bash
# If you want to use the original simpler app
streamlit run app.py
```

---

## 📊 Data Summary

After scraping, you'll have access to:

| Item | Count | Source |
|------|-------|--------|
| Recipes | 1,000,000+ | Beer Analytics |
| Hops | 500+ | Beer Analytics |
| Yeasts | 100+ | Beer Analytics |
| Beer Styles | 100+ | BJCP |
| Fermentables | 200+ | Beer Analytics |

---

## 🔍 Advanced Features

### **Advanced Filtering Dashboard**
- Filter recipes by 7+ criteria
- Filter hops by alpha acids, origin, flavor
- Filter yeasts by type, temp, attenuation
- Filter fermentables by type, color, PPG

### **Analytics & Statistics**
- Total recipe statistics
- Distribution charts (IBU, ABV, Color, OG)
- Statistics by beer style
- Popular items rankings

### **Recipe Builder**
- Choose beer style with guidelines
- Set target parameters (IBU, ABV, color)
- Auto-recommended ingredients
- Generate complete recipes

### **Hop Pairings**
- Select a hop
- See compatible hops
- Based on real recipes

---

## ⚙️ Configuration

### Environment Variables
```bash
# Required
export FIRECRAWL_API_KEY="your_key"

# Optional
export STREAMLIT_THEME_BASE="dark"  # dark or light
export STREAMLIT_LOGGER_LEVEL="info"
```

### Streamlit Config (~/.streamlit/config.toml)
```toml
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#31333F"

[client]
showErrorDetails = true
```

---

## 🐛 Troubleshooting

### Problem: "No data loaded"
**Solution:**
```bash
# 1. Check if data exists
ls data/beer-analytics-full/

# 2. If empty, run scraper again
python scraper_enhanced.py

# 3. Check API key
echo $FIRECRAWL_API_KEY
```

### Problem: "Streamlit won't start"
**Solution:**
```bash
# Reinstall dependencies
source .venv/bin/activate
uv pip install streamlit plotly pandas numpy firecrawl-py

# Try again
streamlit run app_comprehensive.py
```

### Problem: "API key not working"
**Solution:**
```bash
# 1. Verify key at https://www.firecrawl.dev/
# 2. Re-export it
export FIRECRAWL_API_KEY="your_actual_key"

# 3. Check it's set
echo $FIRECRAWL_API_KEY
```

### Problem: "Scraper fails halfway"
**Solution:**
- May hit rate limits on free tier
- Run again, it resumes from where it left off
- Or wait a few hours before re-running

---

## 📈 Next Steps

### For Exploration
1. Run the app: `streamlit run app_comprehensive.py`
2. Go to Home page
3. Explore Beer Styles
4. Search for recipes
5. Check Analytics

### For Learning
1. Visit Beer Styles page
2. Read BJCP guidelines
3. Check recommended hops/yeasts
4. View style statistics

### For Building
1. Use Recipe Builder
2. Choose your style
3. Follow recommendations
4. Generate recipe

---

## 🎯 Common Tasks

### Search for IPA recipes
1. Go to **Recipe Search**
2. Enter style: "IPA"
3. Set IBU: 50-80
4. Click **Search**

### Find best hops for Stout
1. Go to **Beer Styles**
2. Select "American Stout"
3. View **Recommended Hops**
4. Or go to **Hop Library** to explore

### Calculate IBU for a recipe
1. Go to **IBU/ABV/Color**
2. Select hop and amount
3. Set boil time
4. See estimated IBU

### Build a custom recipe
1. Go to **Recipe Builder**
2. Choose beer style
3. Set target IBU/ABV/color
4. Select hops, yeast
5. Generate recipe

---

## 📚 Documentation Structure

- **README_COMPREHENSIVE.md** - Complete feature list & API usage
- **GETTING_STARTED.md** - This guide
- **QUICK_START.md** - Minimal 5-minute setup
- **FIRECRAWL_SETUP.md** - Detailed configuration

---

## 🎉 You're All Set!

Your comprehensive beer analytics platform is ready with:

✅ All Beer Analytics features
✅ 1M+ recipes
✅ Advanced search & filtering
✅ Complete ingredient libraries
✅ Community analytics
✅ Recipe builder
✅ All calculators & tools

### Start Now:
```bash
# 1. Set API key
export FIRECRAWL_API_KEY="your_key"

# 2. Scrape data
python scraper_enhanced.py

# 3. Run app
streamlit run app_comprehensive.py
```

**Visit:** http://localhost:8501

---

## 🍺 Happy Brewing!

Built with ❤️ for homebrewers everywhere
