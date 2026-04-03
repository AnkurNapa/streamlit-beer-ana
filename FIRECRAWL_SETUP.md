# Beer Analytics Integration with Firecrawl

This guide explains how to scrape data from Beer Analytics using Firecrawl and integrate it into your Streamlit app.

## Prerequisites

1. **Get a Firecrawl API Key**
   - Visit https://www.firecrawl.dev/
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Install Dependencies**
   ```bash
   source .venv/bin/activate
   uv pip install firecrawl-py
   ```

## Setup Instructions

### Step 1: Set Your API Key

```bash
# Set environment variable
export FIRECRAWL_API_KEY="your_api_key_here"

# Or add to .env file
echo "FIRECRAWL_API_KEY=your_api_key_here" > .env
```

### Step 2: Scrape Beer Analytics Data

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the scraper to fetch all data from Beer Analytics
python scraper_firecrawl.py
```

This will:
- Scrape hop varieties and characteristics
- Extract yeast strain data
- Get beer style guidelines
- Fetch fermentable/grain information
- Pull recipe data
- Extract trending recipes and hops

Data will be saved to: `data/beer-analytics/`

### Step 3: Use the Data in Streamlit

The data loader automatically detects scraped data and uses it:

```python
from data_loader import DataLoader

loader = DataLoader()

# Load different data types
hops = loader.load_hops()
yeasts = loader.load_yeasts()
recipes = loader.load_recipes()
styles = loader.load_beer_styles()
fermentables = loader.load_fermentables()
trends = loader.load_trends()

# Search recipes
results = loader.search_recipes(style="IPA", ibu_min=50, ibu_max=80)

# Get popular hops
popular = loader.get_popular_hops(limit=10)
```

## Features Enabled

Once data is scraped, your Streamlit app gains:

✅ **Real Recipe Database** - 1M+ recipes from Beer Analytics
✅ **Advanced Recipe Search** - Filter by style, IBU, ABV, color
✅ **Trending Analysis** - See what's popular in the community
✅ **Enhanced Hop Profiles** - Real usage statistics
✅ **Yeast Recommendations** - Based on beer style and recipe
✅ **Fermentable Library** - All grains and malts used
✅ **Smart Pairing Suggestions** - Based on real recipes
✅ **Community Analytics** - Popularity metrics

## Troubleshooting

### API Key Issues
```bash
# Check if FIRECRAWL_API_KEY is set
echo $FIRECRAWL_API_KEY

# If not set, export it
export FIRECRAWL_API_KEY="your_key"
```

### Scraping Fails
- Check your API key is valid
- Verify internet connection
- Try scraping one page at a time for debugging
- Check Firecrawl dashboard for rate limits

### Data Not Loading in Streamlit
- Verify files exist in `data/beer-analytics/`
- Check file names match exactly:
  - hops.json
  - yeasts.json
  - beer_styles.json
  - fermentables.json
  - recipes.json
  - trends.json

## Manual Data Refresh

To refresh data from Beer Analytics:

```bash
source .venv/bin/activate
export FIRECRAWL_API_KEY="your_key"
python scraper_firecrawl.py
```

The Streamlit app will automatically use the latest data (with cache invalidation).

## Rate Limits

- Firecrawl free tier: Limited requests per day
- For large-scale scraping, consider upgrading your plan
- Data is cached locally to minimize API calls

## Next Steps

1. Get your Firecrawl API key
2. Set the environment variable
3. Run `python scraper_firecrawl.py`
4. Your Streamlit app will automatically load the data
5. Start exploring real beer recipes and analytics!
