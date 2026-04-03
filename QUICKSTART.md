# Quick Start Guide

## 1️⃣ Install Dependencies (2 minutes)

```bash
cd /Users/ankur/streamlit_beer_ana
pip install -r requirements.txt
```

## 2️⃣ Run the App (1 minute)

```bash
streamlit run app.py
```

The app will automatically open at `http://localhost:8501` in your browser.

## 3️⃣ Try It Out (5 minutes)

### Scenario 1: Find Hops for Your Beer Style
1. Click **📊 Beer Style Explorer** in the sidebar
2. Select "INDIA PALE ALE (IPA)" category
3. Choose "American IPA" sub-category
4. See recommended hops and characteristics

### Scenario 2: Quick Hop Lookup
1. Click **🎯 Quick Hop Finder**
2. Adjust sliders:
   - IBU: 60 (for bitter IPA)
   - ABV: 6.5% (typical strength)
   - Style: "IPA"
3. Click "Find Hops" button
4. See top 5 compatible hops with flavor profiles

### Scenario 3: Build a Recipe
1. Click **🧪 Recipe Builder**
2. Select your beer style (System auto-fills ABV/IBU ranges)
3. Choose hops for each stage:
   - Bittering (60 min boil)
   - Aroma (5-15 min boil)
   - Dry (post-fermentation)
4. Click "Generate Recipe Summary"

### Scenario 4: Analyze Flavors
1. Click **🔬 Flavor Analysis**
2. Select 2-3 hops you're considering:
   - Citra, Mosaic, Nelson Sauvin
3. See the combined flavor wheel
4. Understand which flavor categories dominate

## 🎯 What You'll Learn

**Quick Hop Finder** shows you:
- Hop compatibility scores
- Alpha acid percentages (bitterness)
- Flavor profiles
- Aroma characteristics

**Beer Style Explorer** teaches you:
- Official BJCP ranges for each style
- What makes a beer "in-style"
- Natural hop pairings for styles

**Flavor Analysis** reveals:
- How hops combine aromatically
- Flavor category distribution
- Complementary hop combinations

**Data Trends** displays:
- Relationships between ABV and IBU
- Beer category characteristics
- Statistical patterns in styles

**Recipe Builder** guides you:
- Step-by-step recipe creation
- Hop scheduling (bittering → aroma → dry)
- Style-appropriate parameters

## 💡 Pro Tips

### For IPA Lovers
- Use American hops: Citra, Simcoe, Cascade
- Target 60-70 IBU and 6-7% ABV
- Dry hop for maximum aroma

### For Classic Styles
- Use noble hops: Saaz, Hallertau, Goldings
- Lower IBU (20-40), classic profiles
- Emphasis on balance over boldness

### For Fruit Flavors
- Nelson Sauvin (white wine, tropical)
- Galaxy (passionfruit, stone fruit)
- Mosaic (berry, tropical)

### For Earthy/Herbal
- Fuggle, Goldings (UK classics)
- Columbus, Magnum (woody notes)
- Saaz (spicy, herbal)

## 🐛 Troubleshooting

**App doesn't start?**
```bash
pip install --upgrade streamlit pandas numpy plotly
```

**Port 8501 in use?**
```bash
streamlit run app.py --server.port 8502
```

**Data files missing?**
The app expects files at:
- `data/bjcp-style-data/csv/beer-vital-statistics-2008.csv`
- `data/bcc-yeast-strains/Yeast Strains.csv` (optional)

## 📊 Understanding the Data

### IBU (International Bitterness Units)
- Measures hop bitterness
- 0-30: Mild (blondes, wheats)
- 30-60: Moderate (pale ales, IPAs)
- 60+: Bold (double IPAs, imperial stouts)

### ABV (Alcohol by Volume)
- Fermentation strength
- 2-4%: Light/session
- 4-6%: Standard
- 6-8%: Strong
- 8%+: Imperial/big beers

### SRM (Standard Reference Method)
- Measures beer color
- 2-5: Pale golden
- 10-20: Amber/brown
- 25-40: Dark/black

### Alpha Acids
- Hop bitterness compound
- 3-5%: Low (aroma hops)
- 5-10%: Medium (dual-purpose)
- 10%+: High (bittering)

## Next Steps

1. ✅ Run the app
2. ✅ Explore Beer Style Explorer
3. ✅ Try Quick Hop Finder with your favorite style
4. ✅ Build a recipe in Recipe Builder
5. ✅ Compare flavor profiles

## Need Help?

Check the full README.md for:
- Feature explanations
- Customization options
- Advanced workflows
- Data sources

Happy brewing! 🍺
