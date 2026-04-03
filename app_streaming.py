"""
Master Brewer - Streaming Streamlit App
Live data from Beer Analytics with session-based caching (no permanent storage)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streaming_loader import StreamingDataLoader

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Master Brewer - Beer Analytics (Streaming)",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Master Brewer - Live Beer Analytics Platform"},
)

# ==================== CUSTOM CSS ====================
st.markdown(
    """
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
    .subtitle {
        font-size: 1.4em;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .card-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #FF6B35;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .cache-status {
        background-color: #fff3cd;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
        font-size: 0.9em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== INITIALIZATION ====================
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Initialize streaming loader
@st.cache_resource
def get_loader():
    """Cached loader instance - reused across reruns"""
    return StreamingDataLoader()

loader = get_loader()

# ==================== SIDEBAR NAVIGATION ====================
st.sidebar.markdown("# 🍺 **MASTER BREWER**")
st.sidebar.markdown("### Live Beer Analytics Platform")
st.sidebar.markdown("---")

# Session info
mem_usage = loader.get_session_memory_usage()
st.sidebar.markdown("### 📊 **SESSION STATUS**")
st.sidebar.markdown(f"""
**Cache Size:** {mem_usage['cache_size_mb']}
**Cached Items:** {mem_usage['cached_items']}
*Data auto-clears on refresh*
""")

if st.sidebar.button("🗑️ Clear Session Cache", use_container_width=True):
    loader.clear_session_cache()
    st.rerun()

st.sidebar.markdown("---")

# Navigation categories
st.sidebar.markdown("### 🏠 **HOME**")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "Home"

st.sidebar.markdown("### 📚 **EXPLORE DATA**")
if st.sidebar.button("🔍 Recipe Search", use_container_width=True):
    st.session_state.page = "Recipe Search"
if st.sidebar.button("🍻 Beer Styles", use_container_width=True):
    st.session_state.page = "Beer Styles"
if st.sidebar.button("🌿 Hop Library", use_container_width=True):
    st.session_state.page = "Hop Library"
if st.sidebar.button("🧬 Yeast Library", use_container_width=True):
    st.session_state.page = "Yeast Library"
if st.sidebar.button("🌾 Fermentables", use_container_width=True):
    st.session_state.page = "Fermentables"

st.sidebar.markdown("### 🔧 **TOOLS & CALCULATORS**")
if st.sidebar.button("⚙️ Advanced Filters", use_container_width=True):
    st.session_state.page = "Advanced Filters"
if st.sidebar.button("📊 Analytics", use_container_width=True):
    st.session_state.page = "Analytics"

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 **TIPS**")
st.sidebar.info(
    "🟢 **Live streaming**: Data loads on-demand from Beer Analytics\n\n"
    "📦 **Session cache**: Cached data vanishes when you refresh\n\n"
    "⚡ **Minimal storage**: No permanent data files needed"
)

# ==================== HOME PAGE ====================
def page_home():
    st.markdown('<h1 class="main-title">🍺 MASTER BREWER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Live Beer Analytics - Session-Based Streaming</p>', unsafe_allow_html=True)

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### ⚡ How It Works

    This platform streams data **live from Beer Analytics** without storing anything permanently:

    - 📡 **Live Streaming**: Fetches data on-demand from Firecrawl API
    - 💾 **Session Cache**: Data cached only during your session (5-min TTL)
    - 🗑️ **Auto-Cleanup**: Cache disappears when you refresh or close browser
    - 🚀 **Zero Storage**: No 4GB+ data files needed
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("### 🔍 **Search**")
        st.markdown("Find 1M+ recipes with advanced filters")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("### 📚 **Learn**")
        st.markdown("Explore beer styles, hops, yeasts & more")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("### 🧪 **Analyze**")
        st.markdown("View community trends & statistics")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Session status
    st.markdown("### 📊 Session Information")
    mem_info = loader.get_session_memory_usage()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cache Size", mem_info["cache_size_mb"])
    with col2:
        st.metric("Cached Items", mem_info["cached_items"])
    with col3:
        st.metric("TTL", "5 minutes")

    if mem_info["items"]:
        st.markdown('<div class="cache-status">', unsafe_allow_html=True)
        st.markdown(f"**Cached:** {', '.join(mem_info['items'][:3])}")
        if len(mem_info["items"]) > 3:
            st.markdown(f"*+ {len(mem_info['items']) - 3} more*")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== RECIPE SEARCH PAGE ====================
def page_recipe_search():
    st.markdown("# 🔍 Recipe Search")
    st.markdown("Search 1M+ recipes with live streaming and filtering")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        style = st.text_input("Beer Style", placeholder="e.g., IPA")
    with col2:
        ibu_min = st.number_input("Min IBU", min_value=0, value=0)
    with col3:
        ibu_max = st.number_input("Max IBU", min_value=0, value=100)
    with col4:
        abv_min = st.number_input("Min ABV", min_value=0.0, value=0.0)

    abv_max = st.number_input("Max ABV", min_value=0.0, value=15.0)

    if st.button("🔍 Search Recipes", use_container_width=True):
        with st.spinner("🔄 Streaming recipes from Beer Analytics..."):
            progress_bar = st.progress(0)

            filters = {
                "style": style if style else None,
                "ibu_min": int(ibu_min) if ibu_min else None,
                "ibu_max": int(ibu_max) if ibu_max else None,
                "abv_min": abv_min if abv_min else None,
                "abv_max": abv_max if abv_max else None,
            }

            recipes = loader.stream_search_with_progress("recipes", filters, progress_bar)

            if not recipes.empty:
                st.success(f"✅ Found {len(recipes)} recipes")
                st.dataframe(recipes, use_container_width=True)

                # Stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg IBU", f"{recipes['ibu'].mean():.1f}" if 'ibu' in recipes.columns else "N/A")
                with col2:
                    st.metric("Avg ABV", f"{recipes['abv'].mean():.1f}%" if 'abv' in recipes.columns else "N/A")
                with col3:
                    st.metric("Total", len(recipes))
            else:
                st.warning("⚠️ No recipes found. Try adjusting filters.")

# ==================== BEER STYLES PAGE ====================
def page_beer_styles():
    st.markdown("# 🍻 Beer Styles")
    st.markdown("Explore BJCP beer style guidelines")

    with st.spinner("📡 Loading beer styles..."):
        styles_df = None
        for chunk in loader.stream_beer_styles():
            if styles_df is None:
                styles_df = chunk
            else:
                styles_df = pd.concat([styles_df, chunk], ignore_index=True)

    if styles_df is not None and not styles_df.empty:
        st.success(f"✅ Loaded {len(styles_df)} beer styles")

        col1, col2 = st.columns(2)
        with col1:
            selected_style = st.selectbox("Select Beer Style", styles_df["name"].unique() if "name" in styles_df.columns else [])

        if selected_style:
            style_data = styles_df[styles_df["name"] == selected_style].iloc[0] if "name" in styles_df.columns else None
            if style_data is not None:
                st.markdown(f"## {selected_style}")
                st.dataframe(style_data)

# ==================== HOP LIBRARY PAGE ====================
def page_hop_library():
    st.markdown("# 🌿 Hop Library")
    st.markdown("Explore 500+ hop varieties with live data")

    col1, col2 = st.columns(2)
    with col1:
        alpha_min = st.number_input("Min Alpha Acids", min_value=0.0, value=0.0)
    with col2:
        alpha_max = st.number_input("Max Alpha Acids", min_value=0.0, value=20.0)

    if st.button("🔍 Find Hops", use_container_width=True):
        with st.spinner("📡 Loading hops from Beer Analytics..."):
            hops_df = None
            for chunk in loader.stream_hops(
                alpha_acids_min=alpha_min if alpha_min > 0 else None,
                alpha_acids_max=alpha_max if alpha_max > 0 else None,
            ):
                if hops_df is None:
                    hops_df = chunk
                else:
                    hops_df = pd.concat([hops_df, chunk], ignore_index=True)

        if hops_df is not None and not hops_df.empty:
            st.success(f"✅ Found {len(hops_df)} hops")
            st.dataframe(hops_df, use_container_width=True)

# ==================== YEAST LIBRARY PAGE ====================
def page_yeast_library():
    st.markdown("# 🧬 Yeast Library")
    st.markdown("Explore 100+ yeast strains")

    yeast_type = st.text_input("Yeast Type", placeholder="e.g., Ale, Lager")

    if st.button("🔍 Find Yeasts", use_container_width=True):
        with st.spinner("📡 Loading yeasts..."):
            yeasts_df = None
            for chunk in loader.stream_yeasts(yeast_type=yeast_type if yeast_type else None):
                if yeasts_df is None:
                    yeasts_df = chunk
                else:
                    yeasts_df = pd.concat([yeasts_df, chunk], ignore_index=True)

        if yeasts_df is not None and not yeasts_df.empty:
            st.success(f"✅ Found {len(yeasts_df)} yeasts")
            st.dataframe(yeasts_df, use_container_width=True)

# ==================== FERMENTABLES PAGE ====================
def page_fermentables():
    st.markdown("# 🌾 Fermentables")
    st.markdown("Explore grains and malts")

    grain_type = st.text_input("Grain Type", placeholder="e.g., Pale Malt, Chocolate")

    if st.button("🔍 Find Grains", use_container_width=True):
        with st.spinner("📡 Loading fermentables..."):
            fermentables_df = None
            for chunk in loader.stream_fermentables(grain_type=grain_type if grain_type else None):
                if fermentables_df is None:
                    fermentables_df = chunk
                else:
                    fermentables_df = pd.concat([fermentables_df, chunk], ignore_index=True)

        if fermentables_df is not None and not fermentables_df.empty:
            st.success(f"✅ Found {len(fermentables_df)} fermentables")
            st.dataframe(fermentables_df, use_container_width=True)

# ==================== ADVANCED FILTERS PAGE ====================
def page_advanced_filters():
    st.markdown("# ⚙️ Advanced Filters")
    st.markdown("Multi-criteria filtering across all ingredients")

    st.info(
        "🎯 **Filter Recipes** by multiple criteria:\n"
        "Style, IBU, ABV, Color, OG, and more"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        style = st.text_input("Style", placeholder="IPA, Stout, etc.")
    with col2:
        ibu_min = st.number_input("IBU Min", min_value=0, value=0)
    with col3:
        ibu_max = st.number_input("IBU Max", min_value=0, value=100)

    abv_min = st.number_input("ABV Min", min_value=0.0, value=0.0)
    abv_max = st.number_input("ABV Max", min_value=0.0, value=15.0)

    if st.button("🔍 Apply Filters", use_container_width=True):
        with st.spinner("🔄 Streaming filtered data..."):
            filters = {
                "style": style if style else None,
                "ibu_min": int(ibu_min) if ibu_min else None,
                "ibu_max": int(ibu_max) if ibu_max else None,
                "abv_min": abv_min if abv_min else None,
                "abv_max": abv_max if abv_max else None,
            }

            results = loader.stream_search_with_progress("recipes", filters)

            if not results.empty:
                st.success(f"✅ Found {len(results)} recipes")
                st.dataframe(results, use_container_width=True)

# ==================== ANALYTICS PAGE ====================
def page_analytics():
    st.markdown("# 📊 Analytics")
    st.markdown("Community trends and statistics")

    st.info("📈 View real-time analytics based on streamed data")

    # Prefetch top items
    with st.spinner("📡 Loading trending data..."):
        col1, col2, col3 = st.columns(3)

        with col1:
            top_hops = loader.prefetch_top_items("hops", limit=10)
            if not top_hops.empty:
                st.markdown("### 🌿 Top Hops")
                st.dataframe(top_hops[["name", "recipes"]] if "recipes" in top_hops.columns else top_hops)

        with col2:
            top_yeasts = loader.prefetch_top_items("yeasts", limit=10)
            if not top_yeasts.empty:
                st.markdown("### 🧬 Top Yeasts")
                st.dataframe(top_yeasts[["name", "recipes"]] if "recipes" in top_yeasts.columns else top_yeasts)

        with col3:
            top_grains = loader.prefetch_top_items("fermentables", limit=10)
            if not top_grains.empty:
                st.markdown("### 🌾 Top Grains")
                st.dataframe(top_grains[["name", "recipes"]] if "recipes" in top_grains.columns else top_grains)

# ==================== PAGE ROUTING ====================
page = st.session_state.page

if page == "Home":
    page_home()
elif page == "Recipe Search":
    page_recipe_search()
elif page == "Beer Styles":
    page_beer_styles()
elif page == "Hop Library":
    page_hop_library()
elif page == "Yeast Library":
    page_yeast_library()
elif page == "Fermentables":
    page_fermentables()
elif page == "Advanced Filters":
    page_advanced_filters()
elif page == "Analytics":
    page_analytics()
else:
    page_home()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
🍺 Master Brewer - Live Beer Analytics Platform
📡 Data streams live from Beer Analytics via Firecrawl
💾 Session-based caching - No permanent storage
🔄 Auto-clears on refresh | Made with ❤️ for homebrewers
</div>
""", unsafe_allow_html=True)
