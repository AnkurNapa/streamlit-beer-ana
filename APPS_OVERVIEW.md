# 🍺 Master Brewer - Apps Overview

Choose the right app for your needs!

---

## Available Apps

### 1. **app_streaming.py** ⭐ Recommended for Most Users
- **Data:** Live streaming from Beer Analytics via Firecrawl
- **Storage:** Zero permanent storage
- **Cache:** 5-minute session cache
- **Best For:** Real-time data, single API source
- **Setup:** Requires `FIRECRAWL_API_KEY` environment variable
- **Performance:** 2-5s first load, <100ms cached

```bash
export FIRECRAWL_API_KEY="your_key"
streamlit run app_streaming.py
```

**Features:**
- ✅ Live streaming from beer-analytics.com
- ✅ Session-based caching (5 min TTL)
- ✅ Auto-cleanup on refresh
- ✅ Memory efficient (10-50MB)
- ✅ 8 pages: Home, Recipe Search, Styles, Hops, Yeasts, Fermentables, Advanced Filters, Analytics

---

### 2. **app_multi_source.py** ⭐ Best for Data Exploration
- **Data:** 20+ GitHub, Kaggle, and JSON sources
- **Storage:** Zero permanent storage
- **Cache:** 5-minute session cache
- **Best For:** Exploring multiple beer datasets, custom sources
- **Setup:** Optional Firecrawl key, optional Kaggle API
- **Performance:** 1-3s per source, <100ms cached

```bash
streamlit run app_multi_source.py
```

**Features:**
- ✅ 10 pre-configured sources (GitHub/JSON/CSV)
- ✅ Custom GitHub CSV/JSON loader
- ✅ Kaggle dataset support
- ✅ Session-based caching
- ✅ 6 pages: Available Sources, Hop DB, Styles, Breweries, 30K Dataset, Custom Source

**Pre-Configured Sources:**
- 🌿 Hop Database (GitHub)
- 🍻 BJCP 2021 Styles (GitHub)
- 🏭 Open Brewery DB (GitHub)
- 🍺 30K Beer Dataset (GitHub)
- 📦 Common Beer Data (GitHub)

**Custom Sources (via UI):**
- Brewtoad 330K recipes
- BrewGr 94K recipes
- Beer Project 70K recipes
- Brewer's Friend 75K/180K (Kaggle)
- Homebrew Recipes (Kaggle)
- Beer Reviews 1.5M (Kaggle)
- And 15+ more!

---

### 3. **app_comprehensive.py** Older Version (Pre-Scraped Data)
- **Data:** Pre-scraped JSON files (4GB+)
- **Storage:** 4GB+ on disk
- **Cache:** File-based (permanent)
- **Best For:** Demo/testing without API
- **Setup:** Run scraper first
- **Performance:** Fast (no API calls)

```bash
# First time: scrape data
python scraper_enhanced.py

# Then run
streamlit run app_comprehensive.py
```

**Features:**
- ✅ 15 pages of features
- ✅ No API calls needed
- ✅ Fast performance
- ✅ Huge data files (4GB+)
- ❌ Stale data (post-scrape only)
- ❌ No live updates

---

## Comparison Table

| Feature | `app_streaming.py` | `app_multi_source.py` | `app_comprehensive.py` |
|---------|-------------|------|-------|
| **Data Source** | Beer Analytics | 20+ sources | Pre-scraped JSON |
| **Storage** | Zero | Zero | 4GB+ |
| **Update Frequency** | Live | Per source | Static |
| **Cache Type** | Session (5 min) | Session (5 min) | File |
| **API Required** | Firecrawl | Kaggle (optional) | None |
| **First Load** | 2-5 sec | 1-3 sec | <1 sec |
| **Cached Load** | <100ms | <100ms | <100ms |
| **Memory** | 10-50MB | 10-50MB | Varies |
| **Pages** | 8 | 6 | 15 |
| **Best For** | Production | Exploration | Demo |

---

## Which App to Choose?

### ✅ Use `app_streaming.py` If:
- You want **live data** from Beer Analytics
- You have a **Firecrawl API key** (free tier available)
- You prefer **minimal storage** (zero disk usage)
- You want **real-time data** that's always fresh
- You're building for **production**
- You like **simplicity** (one data source)

### ✅ Use `app_multi_source.py` If:
- You want to **explore multiple datasets**
- You want **flexibility** to add any GitHub/Kaggle source
- You're doing **research** or **data analysis**
- You want **more features** than streaming version
- You prefer **comparison analysis** across sources
- You want to **experiment** with different data

### ✅ Use `app_comprehensive.py` If:
- You want **no dependencies** (no APIs needed)
- You want **fastest performance** (pre-loaded data)
- You're **testing/demoing** without internet
- You're okay with **4GB+ disk storage**
- You want **15 pages** of features
- You don't need **live updates**

---

## Quick Decision Tree

```
Do you have Firecrawl API key?
├─ YES, want live Beer Analytics data → app_streaming.py ✅
└─ NO, want to explore multiple sources → app_multi_source.py ✅
    └─ Want 15 pages, pre-scraped data → app_comprehensive.py

Do you have lots of disk space?
├─ YES → Use app_comprehensive.py (4GB+)
└─ NO → Use app_streaming.py or app_multi_source.py (zero storage)

Want to explore many datasets?
├─ YES → app_multi_source.py ✅
└─ NO → app_streaming.py ✅
```

---

## Setup Instructions

### For `app_streaming.py`

```bash
# 1. Get Firecrawl API key
# Visit: https://www.firecrawl.dev/

# 2. Set environment variable
export FIRECRAWL_API_KEY="your_key_here"

# 3. Run app
streamlit run app_streaming.py

# 4. Visit: http://localhost:8501
```

### For `app_multi_source.py`

```bash
# Firecrawl API (optional)
export FIRECRAWL_API_KEY="your_key_here"  # For live streaming

# Kaggle API (optional, for Kaggle datasets)
pip install kaggle
# Then get token from: https://www.kaggle.com/settings/account
# Move to: ~/.kaggle/kaggle.json

# Run app
streamlit run app_multi_source.py

# Visit: http://localhost:8501
```

### For `app_comprehensive.py`

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Scrape data (optional, if not already done)
export FIRECRAWL_API_KEY="your_key"
python scraper_enhanced.py

# 3. Run app
streamlit run app_comprehensive.py

# 4. Visit: http://localhost:8501
```

---

## Data Sources by App

### `app_streaming.py`
- Beer Analytics (via Firecrawl)

### `app_multi_source.py`
- **GitHub (10 pre-configured):**
  - Hop Database (500+ hops)
  - BJCP 2021 Styles (100+ styles)
  - Open Brewery DB (5000+ breweries)
  - 30K Beer Dataset (30K beers)
  - Common Beer Data (1000+ items)
  
- **GitHub (Custom - 15+ more):**
  - Brewtoad 330K recipes
  - BrewGr 94K recipes
  - BrewDog DIY 325 recipes
  - Beer Project 70K recipes
  - Beer Recipe Analysis 100K+
  
- **Kaggle (13+ datasets):**
  - Brewer's Friend 75K
  - Brewer's Friend 180K
  - Brewer's Friend Public
  - Homebrew Recipes 40K
  - Homebrew Beer Data 10K
  - Beer Reviews 1.5M
  - Beer Profile & Ratings 100K
  - Beer Brewing Formulas 75K
  - Beer Oasis 100K
  - Craft Beers Dataset 2.4K
  - Beer Production Rankings
  - Beer Consumption São Paulo
  - Yeast Transcriptomics

### `app_comprehensive.py`
- Pre-scraped data from all sources (4GB+)

---

## Memory & Performance

### `app_streaming.py`
- **Memory:** 10-50MB per session
- **First load:** 2-5 seconds
- **Cached load:** <100ms
- **Cache TTL:** 5 minutes
- **Peak usage:** ~50MB

### `app_multi_source.py`
- **Memory:** 10-50MB per session
- **First load:** 1-3 seconds per source
- **Cached load:** <100ms
- **Cache TTL:** 5 minutes per source
- **Peak usage:** ~50MB (cached separately)

### `app_comprehensive.py`
- **Memory:** Varies (500MB+ depending on pages loaded)
- **First load:** <1 second
- **Cached load:** Instant
- **Storage:** 4GB+ permanent
- **Peak usage:** 1GB+

---

## Features Matrix

| Feature | Streaming | Multi | Comprehensive |
|---------|-----------|-------|---------------|
| **Data Streaming** | ✅ | ✅ | ✅ |
| **Live Updates** | ✅ | Partial | ❌ |
| **Multiple Sources** | ❌ | ✅ | ✅ |
| **Session Cache** | ✅ | ✅ | ❌ |
| **Zero Storage** | ✅ | ✅ | ❌ |
| **Recipe Search** | ✅ | ✅ | ✅ |
| **Styles Guide** | ✅ | ✅ | ✅ |
| **Hop Library** | ✅ | ✅ | ✅ |
| **Yeast Library** | ✅ | Partial | ✅ |
| **Advanced Filters** | ✅ | ✅ | ✅ |
| **Analytics** | ✅ | ✅ | ✅ |
| **Flavor Wheel** | ❌ | ❌ | ✅ |
| **IBU Calculator** | ❌ | ❌ | ✅ |
| **ABV Calculator** | ❌ | ❌ | ✅ |
| **Recipe Builder** | ❌ | ❌ | ✅ |

---

## Example Workflows

### Workflow 1: Production Deployment
```
1. Use app_streaming.py
2. Set Firecrawl API key
3. Deploy to Streamlit Cloud
4. Share live URL
5. Zero storage, live data ✅
```

### Workflow 2: Data Analysis
```
1. Use app_multi_source.py
2. Load multiple Kaggle datasets
3. Compare beer styles across sources
4. Export filtered data
5. Explore trends ✅
```

### Workflow 3: Demo/Testing
```
1. Use app_comprehensive.py
2. Pre-scrape all data
3. Demo without internet
4. Test features offline
5. Fast, no API calls ✅
```

### Workflow 4: Research
```
1. Use app_multi_source.py
2. Load 30K dataset from GitHub
3. Load 1.5M reviews from Kaggle
4. Compare beer profiles
5. Statistical analysis ✅
```

---

## Migration Between Apps

### From `app_comprehensive.py` → `app_streaming.py`
- Get Firecrawl API key
- Set `FIRECRAWL_API_KEY` env var
- Run `app_streaming.py`
- Free up 4GB storage ✅

### From `app_streaming.py` → `app_multi_source.py`
- Run `app_multi_source.py`
- No additional setup needed
- Choose different data sources ✅

### From `app_multi_source.py` → `app_streaming.py`
- Set Firecrawl API key
- Run `app_streaming.py`
- Back to single source, live updates ✅

---

## Recommended Setup

### For Most Users: `app_streaming.py`

```bash
# Get free Firecrawl API key (1000 pages/month free)
# Visit: https://www.firecrawl.dev/

# Setup
export FIRECRAWL_API_KEY="your_key"

# Run
streamlit run app_streaming.py

# Deploy to Streamlit Cloud (optional)
# Visit: https://share.streamlit.io/
```

**Benefits:**
- ✅ Simplest setup
- ✅ Live data
- ✅ Zero storage
- ✅ Free tier available
- ✅ Production-ready

---

## Summary

| Task | Best App |
|------|----------|
| Production deployment | `app_streaming.py` |
| Data exploration | `app_multi_source.py` |
| Quick demo | `app_comprehensive.py` |
| Research/analysis | `app_multi_source.py` |
| Real-time data | `app_streaming.py` |
| No storage | `app_streaming.py` or `app_multi_source.py` |
| Maximum features | `app_comprehensive.py` |

---

## Next Steps

### 1️⃣ Choose Your App
- Most users: `app_streaming.py`
- Explorers: `app_multi_source.py`
- Demo/offline: `app_comprehensive.py`

### 2️⃣ Setup
```bash
export FIRECRAWL_API_KEY="your_key"  # Only if using streaming
streamlit run app_streaming.py        # Or app_multi_source.py
```

### 3️⃣ Explore
- Visit http://localhost:8501
- Click around
- Load data
- Have fun! 🍺

### 4️⃣ Deploy (Optional)
```bash
git push origin main
# Then deploy to Streamlit Cloud
```

---

**Ready to choose?** 🍺 Pick your app and start exploring beer data!
