# 🍺 Master Brewer - Complete Beer Analytics Platform

A **production-ready Streamlit platform** for beer analysis, recipe building, ingredient exploration, and water chemistry. Stream data live from 20+ sources with zero permanent storage.

---

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run an App
```bash
# Live Beer Analytics (requires Firecrawl API key)
export FIRECRAWL_API_KEY="your_key_here"
streamlit run app_streaming.py

# OR: Multi-source explorer (no API needed)
streamlit run app_multi_source.py

# OR: Complete ingredients tool (no API needed)
streamlit run app_ingredients.py
```

---

## 📚 Five Production-Ready Apps

### 1. 🎯 **app_streaming.py** — Live Beer Analytics
**Best for:** Real-time data, production deployment

**Data Source:** Beer Analytics (Firecrawl streaming)

**8 Pages:**
- 🏠 **Home** — Overview and session status
- 🔍 **Recipe Search** — Filter 30K+ recipes by style, IBU, ABV
- 🍻 **Beer Styles** — BJCP style guide with characteristic ranges
- 🌿 **Hop Library** — Browse 500+ hops with origin & flavor
- 🧬 **Yeast Library** — 100+ yeast profiles with temp ranges
- 🌾 **Fermentables** — 50+ grain malts with color/yield
- 🔧 **Advanced Filters** — Multi-criteria recipe search
- 📊 **Analytics** — Top ingredients and trends

**Key Features:**
- ✅ Live streaming (no storage)
- ✅ Session-based 5-min cache (auto-clear on refresh)
- ✅ Memory-efficient (10-50MB per session)
- ✅ 2-5s first load, <100ms cached

**Setup:**
```bash
# Get free Firecrawl API key: https://www.firecrawl.dev/
export FIRECRAWL_API_KEY="your_key"
streamlit run app_streaming.py
```

---

### 2. 🌍 **app_multi_source.py** — Multi-Source Data Explorer
**Best for:** Research, data analysis, exploring multiple datasets

**Data Sources:** 10 pre-configured + custom GitHub/Kaggle

**6 Pages:**
- 📋 **Available Sources** — Browse 20+ pre-configured sources
- 🌿 **Hop Database** — GitHub: 500+ hops (kasperg3/HopDatabase)
- 🍻 **Beer Styles** — BJCP 2021 from GitHub
- 🏭 **Breweries** — 5000+ breweries (Open Brewery DB)
- 🍺 **30K Dataset** — 30K beers from GitHub (philipperemy)
- 🔧 **Custom Source** — Load ANY GitHub CSV/JSON or Kaggle dataset

**Pre-Configured Sources (10):**
- Hop Database (500+ hops)
- BJCP 2021 Styles (100+ styles)
- Open Brewery DB (5000+ breweries)
- 30K Beer Dataset (30K beers)
- Common Beer Data (1000+ items)
- Brewtoad 330K recipes
- BrewGr 94K recipes
- Beer Project 70K recipes
- Brewer's Friend datasets (75K, 180K)
- Beer Reviews 1.5M (Kaggle)

**Key Features:**
- ✅ Load from GitHub repos (any CSV/JSON)
- ✅ Load from Kaggle datasets (with API key)
- ✅ Session-based cache (5 min TTL)
- ✅ Filtering & searching across all sources
- ✅ Zero permanent storage

**Setup:**
```bash
# No API needed! (Optional: Kaggle for datasets)
streamlit run app_multi_source.py
```

---

### 3. 🔄 **app_resilient.py** — Fallback & Resilience System
**Best for:** Production reliability, handling data source failures

**Data Sources:** Multi-source with automatic fallback

**6 Pages:**
- 🏠 **Home** — Explain resilient loading
- 🧪 **Test Fallback** — Test the fallback system
- 🌿 **Hops (Resilient)** — Load with automatic fallback
- 🍻 **Styles (Resilient)** — Load with fallback to alternatives
- 🏭 **Breweries (Resilient)** — Load with contextual suggestions
- 📊 **Source Status** — View all attempted sources & results

**Key Features:**
- ✅ When primary source fails → try fallback sources
- ✅ Never shows errors to users → always has data
- ✅ Suggests alternatives if primary unavailable
- ✅ Tracks source status (success/failure) in session
- ✅ Contextual fallback mappings (hops → beer-dataset, etc.)

**Setup:**
```bash
streamlit run app_resilient.py
```

---

### 4. 🧪 **app_ingredients.py** — Complete Ingredients Tool ⭐ NEW
**Best for:** Recipe development, ingredient exploration, brewing calculations

**7 Pages:**
- 🏠 **Home** — Overview
- 🌾 **Malt Library** — 14 classic malts with filters & chart
- 🔄 **Malt Combinations** — Mix malts → calculate SRM color
- 🌿 **Hop Library** — Full hop data + **IBU calculator**
- 🧬 **Yeast Library** — Yeast profiles + **ABV calculator**
- 💧 **Water Chemistry** — 8 profiles + mineral additions
- 🔨 **Recipe Builder** — 5-step recipe creation

**Classic Malts (14):**
Pilsner, Maris Otter, Munich Light, Vienna, Pale Ale, Crystal 20/40/60/80L, Chocolate, Black Patent, Roasted Barley, Flaked Oats, Wheat

**Water Profiles (8):**
Pilsen, Dublin, Burton, London, Munich, Vienna, Generic Soft, Generic Hard

**Mineral Salts (6):**
CaSO₄, CaCl₂, MgSO₄, NaCl, NaHCO₃, CaCO₃

**Built-In Calculators:**
- 🎨 **SRM Color** — Morey formula from malt bill
- 📈 **IBU Estimation** — Tinseth formula from hops
- 🍻 **ABV Calculation** — (OG − FG) × 131.25
- 🧂 **Mineral Additions** — How much salt to add (g per gal)
- 📊 **Gravity Estimation** — Points per gallon from malts

**Key Features:**
- ✅ All calculations built-in (pure Python)
- ✅ Mix up to 10 malts for custom bills
- ✅ Color swatch visualization (hex from SRM)
- ✅ Pre-built water profiles with adjustment sliders
- ✅ 5-step recipe builder with automatic calculations

**Setup:**
```bash
streamlit run app_ingredients.py
```

---

### 5. 📦 **app_comprehensive.py** — Pre-Scraped Version (Older)
**Best for:** Demo, offline testing, fastest performance

**Data:** 4GB+ pre-scraped JSON files

**15 Pages:** All features from streaming app + additional tools

**Key Features:**
- ✅ No API needed
- ✅ Fastest performance (<1 sec load)
- ✅ Works offline
- ❌ Large disk storage (4GB+)
- ❌ Static data (not live)

**Setup:**
```bash
# First time: scrape data
export FIRECRAWL_API_KEY="your_key"
python scraper_enhanced.py

# Then run
streamlit run app_comprehensive.py
```

---

## 📊 Feature Comparison Table

| Feature | Streaming | Multi | Resilient | Ingredients | Comprehensive |
|---------|-----------|-------|-----------|-------------|---------------|
| **Data Source** | Beer Analytics | 20+ sources | Multi | Classic data | Pre-scraped |
| **Storage** | Zero | Zero | Zero | Zero | 4GB+ |
| **Live Data** | ✅ | Partial | ✅ | ✅ | ❌ |
| **API Required** | Firecrawl | Kaggle (opt) | — | — | Firecrawl |
| **Pages** | 8 | 6 | 6 | 7 | 15 |
| **Session Cache** | ✅ | ✅ | ✅ | N/A | ❌ |
| **Memory** | 10-50MB | 10-50MB | 10-50MB | N/A | 500MB+ |
| **SRM Calculator** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **IBU Calculator** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Water Chemistry** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Recipe Builder** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Fallback System** | ❌ | ❌ | ✅ | ❌ | ❌ |

---

## 🎯 Use Cases & Recommendations

### For Production Deployment
→ Use **`app_streaming.py`** or **`app_resilient.py`**
- Live data
- Zero storage
- Auto-fallback on failures
- Deploy to Streamlit Cloud instantly

### For Data Analysis & Research
→ Use **`app_multi_source.py`**
- Access 20+ sources
- Load Kaggle datasets (1.5M+ records)
- Compare across sources
- Export filtered data

### For Recipe Development
→ Use **`app_ingredients.py`**
- Mix malts, calculate color
- Estimate IBU from hops
- Calculate ABV
- Adjust water chemistry
- Build complete recipes

### For Demo/Testing (Offline)
→ Use **`app_comprehensive.py`**
- No internet needed
- Fastest performance
- All features included

---

## 📚 Core Libraries

### Loaders
- **`streaming_loader.py`** — Single-source live streaming (Firecrawl)
- **`multi_source_loader.py`** — Multi-source (GitHub/Kaggle)
- **`resilient_loader.py`** — Fallback system with alternatives
- **`data_loader_enhanced.py`** — Static data operations
- **`scraper_enhanced.py`** — Original web scraper

---

## 🔄 Data Sources (20+)

### Pre-Configured in Multi-Source App
1. **Hop Database** — 500+ hops
2. **BJCP 2021 Styles** — 100+ beer styles
3. **Open Brewery DB** — 5000+ breweries
4. **30K Beer Dataset** — 30K beers
5. **Common Beer Data** — 1000+ items
6. Brewtoad — 330K recipes
7. BrewGr — 94K recipes
8. Beer Project — 70K recipes
9. Brewer's Friend 75K — 75K recipes
10. Brewer's Friend 180K — 180K recipes

### Kaggle Datasets (13+)
- Beer Reviews (1.5M records)
- Brewer's Friend 75K/180K
- Homebrew Recipes (40K)
- Beer Profile & Ratings (100K)
- Beer Brewing Formulas (75K)
- Beer Oasis (100K)
- Craft Beers (2.4K)
- Beer Production Rankings
- Beer Consumption (São Paulo)
- And 4+ more

### Custom Sources
Load ANY public GitHub CSV/JSON or Kaggle dataset through the UI!

---

## 🔧 Architecture Highlights

### Session-Based Streaming
```
User Request
    ↓
Check Session Cache (5 min TTL)
    ↓
Valid? → Return instantly ✅
    ↓
Invalid? → Fetch from API/GitHub/Kaggle
    ↓
Parse Data (JSON/CSV)
    ↓
Apply Filters
    ↓
Yield Chunks (100 items)
    ↓
Call gc.collect() for Memory
    ↓
Cache in Session
    ↓
Return Complete DataFrame ✅
```

### Fallback System
```
Primary Source
    ↓ (fails)
Try Fallback 1
    ↓ (fails)
Try Fallback 2
    ↓ (fails)
Suggest Alternatives
    ↓
Never Error — Always Has Data ✅
```

---

## 📖 Documentation Files

1. **APPS_OVERVIEW.md** — Compare all 5 apps
2. **STREAMING_ARCHITECTURE.md** — How streaming works
3. **MULTI_SOURCE_GUIDE.md** — Load from 20+ sources
4. **GITHUB_SETUP.md** — GitHub setup
5. **DEPLOY_TO_GITHUB.md** — Deploy guide
6. **GETTING_STARTED.md** — Getting started
7. **QUICK_START.md** — 5-minute setup

---

## 🧪 Testing the Ingredients App

### Test Malt Combinations
1. Go to **Malt Combinations** page
2. Select 3-5 classic malts (e.g., Pilsner, Crystal 40, Chocolate)
3. Set weight % per malt
4. See **SRM color** calculated in real-time
5. View color swatch

### Test Water Chemistry
1. Go to **Water Chemistry** page
2. Select Burton profile
3. Adjust Ca/Mg/Na/Cl/SO4/HCO3 sliders
4. See **mineral additions** calculator (g per gallon)
5. Calculate total for 5-gallon batch

### Test Recipe Builder
1. Go to **Recipe Builder** page
2. Pick style (IPA, Pilsner, Porter, etc.)
3. Select malts → calculates OG
4. Select hops → calculates IBU
5. Select yeast → calculates ABV
6. Select water profile
7. Generate complete recipe card with ✅/❌ vs BJCP spec

---

## ⚡ Performance

| Operation | Time |
|-----------|------|
| First load (streaming) | 2-5 sec |
| Cached load | <100 ms |
| Malt combination calc | <10 ms |
| IBU calculation | <1 ms |
| SRM calculation | <1 ms |

---

## 🔐 Security & Storage

- ✅ **Zero permanent files** — All streaming, session-based
- ✅ **Auto-cleanup** — Data cleared on refresh
- ✅ **No credentials stored** — API keys via environment vars only
- ✅ **HTTPS only** — Streamlit Cloud enforces encryption
- ✅ **Open source** — Full transparency

---

## 📦 Requirements

```
streamlit>=1.28.0
pandas>=2.1.0
numpy>=1.24.0
plotly>=5.17.0
firecrawl-py>=0.0.1
python-dotenv>=1.0.0
```

---

## 🚀 Deployment to Streamlit Cloud (Free)

### Step 1: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/streamlit-beer-ana.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy
1. Go to https://share.streamlit.io/
2. Click **New app**
3. Select your repo + branch
4. Main file: `app_streaming.py` (or your choice)
5. Click **Deploy**

### Step 3: Add Secrets (if using Firecrawl)
1. Settings (⚙️) → **Secrets**
2. Add:
```
FIRECRAWL_API_KEY=your_actual_key_here
```

---

## 💡 Example Workflows

### Workflow 1: Build an IPA
1. **app_ingredients.py** → Malt Combinations
2. Select Pilsner (70%) + Crystal 40L (20%) + Black Patent (10%)
3. See SRM = 15 (amber-brown)
4. Go to Recipe Builder
5. Select Cascade, Centennial hops
6. Select Ale Yeast
7. Generate recipe

### Workflow 2: Analyze Water Chemistry
1. **app_ingredients.py** → Water Chemistry
2. Select **Burton** (high sulfate)
3. Adjust to **Pilsen** (soft water)
4. See CaCO₃ and NaHCO₃ additions needed
5. Calculate total minerals for 10-gallon batch

### Workflow 3: Find Hops for High-IBU Beer
1. **app_multi_source.py** → Hop Database
2. Filter by high alpha acids (12%+)
3. **app_streaming.py** → Advanced Filters
4. Search recipes with 80+ IBU
5. See which hops used historically

### Workflow 4: Compare Yeast Strains
1. **app_streaming.py** → Yeast Library
2. Compare attenuation & temperature ranges
3. Use **app_ingredients.py** → Yeast Library
4. ABV calculator for different yeasts
5. Choose best fit for your style

---

## 🛠️ Development

### Add a New Data Source
Edit `multi_source_loader.py`:
```python
self.sources['my-source'] = {
    'type': 'csv',
    'url': 'https://raw.githubusercontent.com/...',
    'description': 'My custom data'
}
```

### Add a New Calculator
Edit `app_ingredients.py` and add function:
```python
def calculate_my_metric(param1, param2):
    return result
```

### Add a New Page
In any app file:
```python
def page_new():
    st.markdown("# New Page")
    # Your code here

if page == "new":
    page_new()
```

---

## 📞 Support & Feedback

- **GitHub Issues:** Report bugs or suggest features
- **Discussions:** Ask questions, share recipes
- **Pull Requests:** Contribute improvements

---

## 📄 License

Open source — feel free to modify and extend!

---

## 🍻 Cheers!

Made for beer enthusiasts and homebrewers. Happy brewing! 🍺

**GitHub:** https://github.com/AnkurNapa/streamlit-beer-ana

**Live Demo:** https://share.streamlit.io/AnkurNapa/streamlit-beer-ana/app_streaming.py (after deployment)
