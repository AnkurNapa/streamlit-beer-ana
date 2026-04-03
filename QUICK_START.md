# Master Brewer - Quick Start Guide

Your Streamlit app has been enhanced with **real Beer Analytics data** integration!

## 🚀 Quick Setup (5 minutes)

### 1️⃣ Get Firecrawl API Key
- Go to https://www.firecrawl.dev/
- Sign up (free account)
- Copy your API key

### 2️⃣ Scrape Beer Analytics Data
```bash
# Set your API key
export FIRECRAWL_API_KEY="your_api_key_here"

# Or create .env file with:
# FIRECRAWL_API_KEY=your_api_key_here

# Activate environment and run scraper
source .venv/bin/activate
python scraper_firecrawl.py
```

### 3️⃣ Start Streamlit App
```bash
source .venv/bin/activate
streamlit run app.py
```

**That's it!** Your app now has access to 1M+ real recipes.

---

## 📊 New Features Added

### 🔍 **Recipe Search**
- Search 1M+ brewing recipes from Beer Analytics
- Filter by style, IBU, ABV, color
- View recipe statistics and trends

### 📈 **Trending**
- See trending hops in the community
- Popular beer styles
- Most used hop combinations

### 🧬 **Yeasts Library**
- 100+ yeast strains from Beer Analytics
- Attenuation, temperature range, flavor profile
- Usage statistics in recipes

### 🌾 **Fermentables Library**
- All grains and malts used in Beer Analytics
- Filter by grain type
- Popularity charts

### 📉 **Community Statistics**
- Total recipes and hops database stats
- IBU and ABV distribution
- Average values across the community

---

## 📁 New Files Created

```
├── scraper_firecrawl.py       # Scraper for Beer Analytics
├── data_loader.py             # Data loader for scraped data
├── FIRECRAWL_SETUP.md         # Detailed setup guide
└── QUICK_START.md             # This file
```

---

## 🗂️ Data Structure

After scraping, you'll have:
```
data/
└── beer-analytics/
    ├── hops.json              # 500+ hop varieties
    ├── yeasts.json            # 100+ yeast strains
    ├── beer_styles.json       # Beer style guidelines
    ├── fermentables.json      # Grains and malts
    ├── recipes.json           # 1M+ recipes
    └── trends.json            # Trending data
```

---

## 💡 Tips

- **First time?** Start with Recipe Search to explore real recipes
- **Data refresh:** Run `scraper_firecrawl.py` anytime to update data
- **No internet?** Scraped data is cached locally
- **Free tier** sufficient for exploration; upgrade if you hit limits

---

## 🔧 Troubleshooting

**Data not loading?**
```bash
# Check if files exist
ls data/beer-analytics/

# Check if scraper ran successfully
python scraper_firecrawl.py
```

**API key issues?**
```bash
# Verify key is set
echo $FIRECRAWL_API_KEY

# Set it if missing
export FIRECRAWL_API_KEY="your_key"
```

**Streamlit won't start?**
```bash
# Reinstall dependencies
source .venv/bin/activate
uv pip install streamlit plotly pandas numpy firecrawl-py
streamlit run app.py
```

---

## 📚 More Info

- Full setup: See `FIRECRAWL_SETUP.md`
- Beer Analytics: https://www.beer-analytics.com/
- Firecrawl Docs: https://www.firecrawl.dev/docs

---

**Ready to brew? Start with Recipe Search!** 🍺
