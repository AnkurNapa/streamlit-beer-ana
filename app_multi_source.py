"""
Master Brewer - Multi-Source Edition
Stream from 20+ GitHub, Kaggle, and JSON data sources
"""

import streamlit as st
import pandas as pd
from multi_source_loader import MultiSourceLoader

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Master Brewer - Multi-Source",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
.main-title {
    font-size: 3.5em;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(135deg, #FF6B35, #FFA500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}
.source-box {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #FF6B35;
    margin: 10px 0;
}
.cache-status {
    background-color: #fff3cd;
    padding: 12px;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZATION ====================
@st.cache_resource
def get_loader():
    return MultiSourceLoader()

loader = get_loader()

# ==================== SIDEBAR ====================
st.sidebar.markdown("# 🍺 **MASTER BREWER**")
st.sidebar.markdown("### Multi-Source Beer Analytics")
st.sidebar.markdown("---")

# Memory status
mem_info = loader.get_session_memory_usage()
st.sidebar.markdown("### 📊 **SESSION**")
st.sidebar.markdown(f"""
Cache: {mem_info['cache_size_mb']}
Items: {mem_info['cached_items']}
""")

if st.sidebar.button("🗑️ Clear Cache", use_container_width=True):
    loader.clear_session_cache()
    st.rerun()

st.sidebar.markdown("---")

# Page selector
st.sidebar.markdown("### 📚 **PAGES**")
if st.sidebar.button("📊 Available Sources", use_container_width=True):
    st.session_state.page = "sources"
if st.sidebar.button("🌿 Hop Database", use_container_width=True):
    st.session_state.page = "hops"
if st.sidebar.button("🍻 Beer Styles", use_container_width=True):
    st.session_state.page = "styles"
if st.sidebar.button("🏭 Breweries", use_container_width=True):
    st.session_state.page = "breweries"
if st.sidebar.button("🍺 30K Beer Dataset", use_container_width=True):
    st.session_state.page = "beer-dataset"
if st.sidebar.button("🔧 Custom Source", use_container_width=True):
    st.session_state.page = "custom"

if "page" not in st.session_state:
    st.session_state.page = "sources"

# ==================== AVAILABLE SOURCES PAGE ====================
def page_sources():
    st.markdown('<h1 class="main-title">📊 Available Data Sources</h1>', unsafe_allow_html=True)
    st.markdown("Stream from 20+ GitHub, Kaggle, and JSON sources")

    st.info("✅ **All sources stream directly** - No downloads, no storage needed!")

    # Built-in sources
    st.markdown("## Built-In Sources (Pre-configured)")
    sources_df = loader.list_sources()
    st.dataframe(sources_df, use_container_width=True)

    # Custom sources
    st.markdown("## Custom GitHub/Kaggle Sources")
    st.markdown("""
    **Available:**
    - Brewtoad (330K BeerXML) — https://github.com/scheb/brewtoad-beer-recipes
    - BrewGr (94K BeerXML) — https://github.com/scheb/brewgr-beer-recipes
    - BrewDog DIY Dog (325 BeerXML) — https://github.com/stuartraetaylor/diydog-beerxml
    - Beer Project 70K (CSV) — https://github.com/realsaul00/beer_project
    - Beer Recipe Analysis — https://github.com/scheb/beer-recipe-analysis
    - Brewer's Friend 75K (Kaggle) — jtrofe/beer-recipes
    - Brewer's Friend 180K (Kaggle) — angeredsquid/brewers-friend-beer-recipes
    - Homebrew Recipes (Kaggle) — matiasmiche/homebrew-beer-recipes
    - Homebrew Beer Data (Kaggle) — basaltier/homebrew-beer-data
    - Beer Reviews 1.5M (Kaggle) — rdoume/beerreviews
    - Beer Profile & Ratings (Kaggle) — ruthgn/beer-profile-and-ratings-data-set
    - Craft Beers (Kaggle) — nickhould/craft-cans
    - Beer Production (Kaggle) — thedevastator/annual-beer-production-rankings

    👉 Use the **Custom Source** page to load any of these!
    """)

# ==================== HOP DATABASE PAGE ====================
def page_hops():
    st.markdown("# 🌿 Hop Database")
    st.markdown("From: https://github.com/kasperg3/HopDatabase")

    col1, col2 = st.columns(2)
    with col1:
        hop_name = st.text_input("Hop Name", placeholder="e.g., Cascade")

    if st.button("🔍 Find Hops", use_container_width=True):
        with st.spinner("📡 Streaming hops..."):
            filters = {"name": hop_name} if hop_name else None
            hops_df = None

            for chunk in loader.stream_hops(filters=filters):
                if hops_df is None:
                    hops_df = chunk
                else:
                    hops_df = pd.concat([hops_df, chunk], ignore_index=True)

        if hops_df is not None and not hops_df.empty:
            st.success(f"✅ Found {len(hops_df)} hops")
            st.dataframe(hops_df, use_container_width=True)
        else:
            st.warning("⚠️ No hops found")

# ==================== BEER STYLES PAGE ====================
def page_styles():
    st.markdown("# 🍻 Beer Styles")
    st.markdown("From: https://github.com/beerjson/bjcp-json")

    if st.button("📥 Load BJCP 2021 Styles", use_container_width=True):
        with st.spinner("📡 Loading beer styles..."):
            styles_df = None

            for chunk in loader.stream_bjcp_styles():
                if styles_df is None:
                    styles_df = chunk
                else:
                    styles_df = pd.concat([styles_df, chunk], ignore_index=True)

        if styles_df is not None and not styles_df.empty:
            st.success(f"✅ Loaded {len(styles_df)} styles")
            st.dataframe(styles_df, use_container_width=True)
        else:
            st.warning("⚠️ No data loaded")

# ==================== BREWERIES PAGE ====================
def page_breweries():
    st.markdown("# 🏭 Breweries")
    st.markdown("From: https://github.com/openbrewerydb/openbrewerydb")

    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City", placeholder="e.g., Denver")
    with col2:
        state = st.text_input("State", placeholder="e.g., Colorado")

    if st.button("🔍 Find Breweries", use_container_width=True):
        with st.spinner("📡 Streaming breweries..."):
            filters = {}
            if city:
                filters["city"] = city
            if state:
                filters["state"] = state

            breweries_df = None

            for chunk in loader.stream_breweries(filters=filters if filters else None):
                if breweries_df is None:
                    breweries_df = chunk
                else:
                    breweries_df = pd.concat([breweries_df, chunk], ignore_index=True)

        if breweries_df is not None and not breweries_df.empty:
            st.success(f"✅ Found {len(breweries_df)} breweries")
            st.dataframe(breweries_df, use_container_width=True)
        else:
            st.warning("⚠️ No breweries found")

# ==================== BEER DATASET PAGE ====================
def page_beer_dataset():
    st.markdown("# 🍺 Beer Dataset (30K)")
    st.markdown("From: https://github.com/philipperemy/beer-dataset")

    col1, col2 = st.columns(2)
    with col1:
        beer_type = st.text_input("Beer Style", placeholder="e.g., IPA")
    with col2:
        brewery = st.text_input("Brewery", placeholder="e.g., Dogfish")

    if st.button("🔍 Search Beers", use_container_width=True):
        with st.spinner("📡 Streaming beers..."):
            filters = {}
            if beer_type:
                filters["style"] = beer_type
            if brewery:
                filters["brewery"] = brewery

            beers_df = None

            for chunk in loader.stream_beer_dataset_30k(filters=filters if filters else None):
                if beers_df is None:
                    beers_df = chunk
                else:
                    beers_df = pd.concat([beers_df, chunk], ignore_index=True)

        if beers_df is not None and not beers_df.empty:
            st.success(f"✅ Found {len(beers_df)} beers")
            st.dataframe(beers_df, use_container_width=True)
        else:
            st.warning("⚠️ No beers found")

# ==================== CUSTOM SOURCE PAGE ====================
def page_custom():
    st.markdown("# 🔧 Custom Data Source")
    st.markdown("Load from any GitHub repo or Kaggle dataset")

    st.markdown("## Option 1: GitHub CSV")
    st.markdown("Example: https://github.com/scheb/brewtoad-beer-recipes/recipes.csv")

    col1, col2 = st.columns(2)
    with col1:
        github_repo = st.text_input(
            "GitHub URL",
            placeholder="https://github.com/user/repo",
        )
    with col2:
        csv_file = st.text_input(
            "File Path",
            placeholder="recipes.csv",
        )

    if st.button("📥 Load GitHub CSV", use_container_width=True):
        if github_repo and csv_file:
            with st.spinner("📡 Loading from GitHub..."):
                data_df = None

                try:
                    for chunk in loader.stream_github_csv(github_repo, csv_file):
                        if data_df is None:
                            data_df = chunk
                        else:
                            data_df = pd.concat([data_df, chunk], ignore_index=True)

                    if data_df is not None and not data_df.empty:
                        st.success(f"✅ Loaded {len(data_df)} rows")
                        st.dataframe(data_df, use_container_width=True)
                    else:
                        st.warning("⚠️ No data loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Enter both GitHub URL and file path")

    st.markdown("---")
    st.markdown("## Option 2: Kaggle Dataset")
    st.info(
        "Requires: `pip install kaggle` and Kaggle API key setup\n\n"
        "Get key: https://www.kaggle.com/settings/account"
    )

    col1, col2 = st.columns(2)
    with col1:
        kaggle_id = st.text_input(
            "Dataset ID",
            placeholder="jtrofe/beer-recipes",
        )
    with col2:
        kaggle_file = st.text_input(
            "File Name",
            placeholder="recipes.csv",
        )

    if st.button("📥 Load Kaggle Dataset", use_container_width=True):
        if kaggle_id and kaggle_file:
            with st.spinner("📡 Downloading from Kaggle..."):
                data_df = None

                try:
                    for chunk in loader.stream_kaggle_dataset(kaggle_id, kaggle_file):
                        if data_df is None:
                            data_df = chunk
                        else:
                            data_df = pd.concat([data_df, chunk], ignore_index=True)

                    if data_df is not None and not data_df.empty:
                        st.success(f"✅ Loaded {len(data_df)} rows")
                        st.dataframe(data_df, use_container_width=True)
                    else:
                        st.warning("⚠️ No data loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Enter both Dataset ID and file name")

    st.markdown("---")
    st.markdown("## Recommended Public Datasets")
    st.markdown("""
    **GitHub:**
    - Brewtoad: `scheb/brewtoad-beer-recipes` → `data/recipes.csv`
    - Beer Project 70K: `realsaul00/beer_project` → `data.csv`

    **Kaggle:**
    - Beer Recipes 75K: `jtrofe/beer-recipes` → `recipeData.csv`
    - Beer Recipes 180K: `angeredsquid/brewers-friend-beer-recipes` → `recipes.csv`
    - Homebrew Recipes: `matiasmiche/homebrew-beer-recipes` → `recipes.csv`
    - Beer Reviews 1.5M: `rdoume/beerreviews` → `beer_reviews.csv`
    """)

# ==================== PAGE ROUTING ====================
page = st.session_state.page

if page == "sources":
    page_sources()
elif page == "hops":
    page_hops()
elif page == "styles":
    page_styles()
elif page == "breweries":
    page_breweries()
elif page == "beer-dataset":
    page_beer_dataset()
elif page == "custom":
    page_custom()
else:
    page_sources()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
🍺 Master Brewer - Multi-Source Beer Analytics
📡 Stream from 20+ GitHub, Kaggle & JSON sources
💾 Session-based caching - No permanent storage
🔄 Auto-clears on refresh
</div>
""", unsafe_allow_html=True)
