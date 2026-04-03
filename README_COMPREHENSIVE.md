# Master Brewer - Complete Beer Analytics Platform

A comprehensive Streamlit application that integrates all features from Beer Analytics, providing a complete brewing platform with 1M+ recipes, advanced filtering, analytics, and tools.

## 🚀 Features Included

### 📚 **Data & Exploration**
- ✅ **Recipe Search** - 1M+ recipes with advanced filtering
- ✅ **Beer Styles Guide** - BJCP guidelines for all styles
- ✅ **Hop Library** - 500+ hops with pairings & usage data
- ✅ **Yeast Library** - 100+ yeast strains with profiles
- ✅ **Fermentables Library** - Grains & malts database

### 🔧 **Tools & Calculators**
- ✅ **Advanced Filters** - Multi-criteria filtering for all ingredients
- ✅ **IBU Calculator** - Calculate bitterness units
- ✅ **ABV Calculator** - Calculate alcohol by volume
- ✅ **Color Chart** - SRM color reference
- ✅ **Hop Pairings** - Find compatible hops
- ✅ **Flavor Wheel** - Flavor profile visualization

### 📊 **Analytics & Insights**
- ✅ **Community Statistics** - Overall brewing statistics
- ✅ **Trending** - Popular hops, yeasts, styles
- ✅ **Popular Items** - Top used ingredients
- ✅ **Distribution Charts** - IBU, ABV, Color distributions

### 🧪 **Building**
- ✅ **Recipe Builder** - Step-by-step recipe creation
- ✅ **Style-Based Recommendations** - Suggested ingredients
- ✅ **Recipe Generator** - Auto-generate recipes

---

## 📋 Quick Start (5 Minutes)

### 1️⃣ Get Firecrawl API Key
```bash
# Visit: https://www.firecrawl.dev/
# Sign up → Copy API key
```

### 2️⃣ Set API Key
```bash
export FIRECRAWL_API_KEY="your_api_key_here"
```

Or create `.env` file:
```
FIRECRAWL_API_KEY=your_api_key_here
```

### 3️⃣ Scrape All Beer Analytics Data
```bash
source .venv/bin/activate
python scraper_enhanced.py
```

This scrapes:
- 500+ hop varieties with detailed profiles
- 100+ yeast strains with characteristics
- BJCP beer style guidelines
- Grains and fermentables database
- 1M+ community recipes with stats
- Trending and popular items

Data saved to: `data/beer-analytics-full/`

### 4️⃣ Run the Comprehensive App
```bash
streamlit run app_comprehensive.py
```

**Open:** http://localhost:8501

---

## 📁 File Structure

```
├── app_comprehensive.py          # Main comprehensive app
├── scraper_enhanced.py           # Complete data scraper
├── data_loader_enhanced.py       # Advanced data loader
├── README_COMPREHENSIVE.md       # This file
├── QUICK_START.md               # Quick start guide
├── FIRECRAWL_SETUP.md           # Detailed setup
│
├── data/
│   └── beer-analytics-full/     # Scraped data
│       ├── hops_detailed.json
│       ├── yeasts_detailed.json
│       ├── beer_styles_detailed.json
│       ├── fermentables_detailed.json
│       ├── recipes_advanced.json
│       └── search_options.json
│
└── .venv/                        # Virtual environment
```

---

## 🎯 Pages & Features

### 🏠 **Home**
- Overview and navigation
- Quick stats
- Feature highlights

### 🔍 **Recipe Search**
- Search 1M+ recipes
- Filter by: style, IBU, ABV, color, OG
- View statistics and distributions
- Sorted results

### 🍻 **Beer Styles Guide**
- BJCP guidelines for 100+ styles
- IBU/ABV/Color ranges
- Recommended hops & yeasts
- Overall impression & characteristics

### 🌿 **Hop Library**
- Detailed profiles for 500+ hops
- Alpha & beta acids
- Flavor & aroma profiles
- Pairing recommendations
- Dosage guidelines

### 🧬 **Yeast Library**
- 100+ yeast strains
- Fermentation temperature range
- Attenuation & flocculation
- Best beer styles
- Alcohol tolerance

### 🌾 **Fermentables**
- Grains & malts database
- Color & PPG values
- Flavor profiles
- Typical usage percentages
- Popularity charts

### ⚙️ **Advanced Filters**
- **Recipe Filters:** Style, IBU, ABV, Color, OG/FG
- **Hop Filters:** Alpha acids, origin, purpose, flavor
- **Yeast Filters:** Type, temperature, attenuation, flocculation
- **Fermentables Filters:** Type, color, PPG

### 📊 **Analytics**
- Total recipes & statistics
- Average IBU/ABV/Color
- Distribution charts
- Statistics by beer style

### 🔥 **Trending**
- Popular hops (top 10)
- Popular yeasts (top 10)
- Popular grains (top 10)

### 🏆 **Popular Items**
- Top hops by usage
- Top yeasts by usage
- Top grains by usage
- Graphical comparisons

### 🎨 **Flavor Wheel**
- Compare multiple hops
- Flavor profile visualization

### 💧 **IBU/ABV/Color**
- IBU calculator with hop selection
- ABV calculator (OG/FG)
- SRM color reference chart

### 🤝 **Hop Pairings**
- Select a hop
- View compatible hops
- Based on community recipes

### 📋 **Recipe Builder**
- Choose beer style
- Set recipe parameters
- Select ingredients
- Auto-generate recipes
- Uses style guidelines & recommendations

---

## 🔧 Advanced Usage

### Custom Data Filtering

```python
from data_loader_enhanced import EnhancedDataLoader

loader = EnhancedDataLoader()

# Filter recipes by multiple criteria
recipes = loader.filter_recipes(
    style="IPA",
    ibu_min=50,
    ibu_max=80,
    abv_min=6.0,
    abv_max=7.5
)

# Filter hops
hops = loader.filter_hops(
    alpha_acids_min=10,
    alpha_acids_max=15,
    origin="USA",
    flavor="citrus"
)

# Get recommendations for a style
recommendations = {
    "hops": loader.get_recommended_hops("IPA"),
    "yeasts": loader.get_recommended_yeasts("IPA"),
}

# Get statistics
stats = loader.get_recipe_statistics()
style_stats = loader.get_style_statistics()
```

### Refresh Data

```bash
# Scrape latest data from Beer Analytics
export FIRECRAWL_API_KEY="your_key"
python scraper_enhanced.py
```

---

## 🐛 Troubleshooting

### API Key Issues
```bash
# Verify key is set
echo $FIRECRAWL_API_KEY

# If not set
export FIRECRAWL_API_KEY="your_key"
```

### Data Not Loading
```bash
# Check if files exist
ls data/beer-analytics-full/

# Re-run scraper
python scraper_enhanced.py
```

### Streamlit Won't Start
```bash
# Reinstall dependencies
source .venv/bin/activate
uv pip install streamlit plotly pandas numpy firecrawl-py

# Run again
streamlit run app_comprehensive.py
```

### Scraper Fails
- Verify API key is valid (at https://www.firecrawl.dev/)
- Check internet connection
- Try running once more (rate limiting may apply)
- Check Firecrawl dashboard for usage limits

---

## 📊 Data Structure

### Hops Data
```json
{
  "name": "Citra",
  "alpha_acids": 12.5,
  "beta_acids": 3.5,
  "origin": "USA",
  "purpose": "Bittering",
  "aroma": ["grapefruit", "lemon"],
  "flavor": ["citrus", "tropical"],
  "pairs_well_with": ["Mosaic", "Amarillo"],
  "recipes": 15234,
  "bittering_oz": "1.0-1.5",
  "aroma_oz": "0.5-1.0",
  "dry_hop_oz": "1.0-2.0"
}
```

### Yeasts Data
```json
{
  "name": "Wyeast 1056",
  "type": "Ale",
  "flavor_profile": "Clean, slightly fruity",
  "temperature_min": 60,
  "temperature_max": 72,
  "attenuation_min": 73,
  "attenuation_max": 77,
  "flocculation": "Medium",
  "alcohol_tolerance": 9,
  "recipes": 8923,
  "best_for": ["American Pale Ale", "IPA"]
}
```

### Beer Styles Data
```json
{
  "name": "American IPA",
  "category": "Pale Ale",
  "ibu_min": 40,
  "ibu_max": 70,
  "abv_min": 6.3,
  "abv_max": 7.8,
  "color_min": 6,
  "color_max": 15,
  "og_min": 1.056,
  "og_max": 1.075,
  "recommended_hops": ["Centennial", "Cascade", "Citra"],
  "recommended_yeasts": ["Wyeast 1056", "Safale US-05"],
  "recipes": 45678
}
```

---

## 🌟 Tips & Best Practices

1. **Start with Home Page** - Get familiar with the interface
2. **Use Recipe Search** - Explore existing recipes for inspiration
3. **Check Style Guidelines** - Understand BJCP standards
4. **Use Advanced Filters** - Narrow down to your preferences
5. **View Analytics** - See what's popular in the community
6. **Use Recipe Builder** - Create recipes following guidelines
7. **Check Hop Pairings** - Find complementary ingredients

---

## 📚 Additional Resources

- **Beer Analytics:** https://www.beer-analytics.com/
- **Firecrawl:** https://www.firecrawl.dev/
- **BJCP Styles:** https://www.bjcp.org/
- **Homebrew Talk:** https://www.homebrewtalk.com/

---

## 🎉 You're Ready!

Your comprehensive beer brewing platform is now complete with:
- ✅ 1M+ recipes from the community
- ✅ Advanced search & filtering
- ✅ Complete ingredient libraries
- ✅ Community analytics
- ✅ Recipe builder
- ✅ All tools & calculators

**Start brewing!** 🍺

---

## 📝 Version Info

- **Streamlit:** Latest
- **Plotly:** For visualization
- **Pandas:** Data manipulation
- **Firecrawl:** Data scraping

---

**Built with ❤️ for homebrewers everywhere**
