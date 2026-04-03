# 🍺 Master Brewer - Beer Data Assistant

A Streamlit app for beer analysis, hop recommendations, and beer recipe building powered by real BJCP beer style data.

## Features

### 🎯 Quick Hop Finder
- Input your target IBU, ABV, and beer style
- Get recommendations for the top 5 compatible hops
- View detailed flavor profiles and aroma characteristics for each hop

### 📊 Beer Style Explorer
- Browse all BJCP beer styles organized by category
- View characteristic ranges (IBU, ABV, SRM, OG)
- Get hop recommendations tailored to each beer style

### 🔬 Flavor Analysis
- Analyze and compare flavor profiles of multiple hops
- Interactive spider/radar charts showing flavor distribution
- Combine multiple hops to see the resulting flavor blend

### 📈 Data Trends
- Scatter plots showing relationships between beer characteristics
- Box plots of ABV distribution by beer category
- Statistical summaries of beer style data

### 🧪 Recipe Builder
- Guided workflow to create custom beer recipes
- Select beer style with automatic parameter ranges
- Choose bittering, aroma, and dry hops for your recipe
- Generate formatted recipe summaries

## Installation

### 1. Clone/Download the Project
```bash
cd streamlit_beer_ana
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Data Sources

- **Beer Styles**: BJCP (Beer Judge Certification Program) 2008 guidelines
  - IBU, ABV, SRM, and gravity ranges for all official beer styles
- **Hop Database**: Common brewing hops with:
  - Alpha acid percentages
  - Flavor profiles
  - Aroma characteristics
  - Geographic origin
- **Yeast Strains**: BCC yeast strain data

## Navigation

Use the sidebar to switch between pages:
1. **Quick Hop Finder** - Fast recommendations
2. **Beer Style Explorer** - Browse BJCP styles
3. **Flavor Analysis** - Compare hop profiles
4. **Data Trends** - Statistical analysis
5. **Recipe Builder** - Create your recipe

## How Hop Recommendations Work

The app scores hops based on:
- **Alpha Acids**: Matches bittering requirements for IBU targets
- **Flavor Profile**: Considers aromatic compounds
- **Alcohol Compatibility**: Pairs well with target ABV
- **Beer Style**: Historical usage and compatibility

## Example Workflows

### Create an IPA
1. Go to **Beer Style Explorer**
2. Select "India Pale Ale (IPA)" → "American IPA"
3. Check recommended hops (typically citrus/pine varieties)
4. Go to **Recipe Builder** and set ABV 5.5-7.5%, IBU 40-70
5. Select recommended hops for different stages

### Find Hops for High-Gravity Beer
1. Go to **Quick Hop Finder**
2. Set ABV to 8%+
3. Set IBU to 50-70
4. View recommendations with Alpha acid profiles

### Analyze Flavor Combinations
1. Go to **Flavor Analysis**
2. Select multiple complementary hops (e.g., Citra, Mosaic, Nelson Sauvin)
3. View combined flavor wheel
4. See distribution of flavor categories

## Tips for Homebrewers

- **Bittering Hops** (high AA): Columbus, Magnum, Simcoe
- **Aroma Hops** (low AA): Cascade, Saaz, Hallertau
- **Noble Hops**: Saaz, Hallertau, Goldings (traditional European)
- **Modern Hops**: Citra, Mosaic, Galaxy (bold, fruity profiles)

## Customization

### Add More Hops
Edit the `load_hop_database()` function in `app.py`:
```python
'New Hop Name': {
    'AA': 12.5,
    'Beta': 3.5,
    'flavor': ['citrus', 'tropical'],
    'aroma': ['grapefruit'],
    'origin': 'Country',
    'alpha_acids': 12.5
}
```

### Add More Yeast
Place additional yeast data CSV files in the `data/` directory and modify the app to load them.

## Requirements

- Python 3.8+
- Streamlit 1.28+
- Pandas 2.1+
- NumPy 1.24+
- Plotly 5.17+

## Browser Support

Works best in:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Troubleshooting

**App won't start**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

**Data not loading**
- Verify `data/` directory exists with CSV files
- Check file paths in the `load_*()` functions

**Charts not displaying**
- Update Plotly: `pip install --upgrade plotly`
- Clear browser cache and refresh

## Future Features

- [ ] YeastPairing analyzer
- [ ] Water chemistry calculator
- [ ] Mash profile builder
- [ ] Fermentation timeline tracker
- [ ] Export recipes to BeerXML
- [ ] Save favorite recipes
- [ ] Community recipe sharing

## License

Open source - feel free to modify and extend!

## Cheers! 🍻

Made for beer enthusiasts and homebrewers. Enjoy crafting!
