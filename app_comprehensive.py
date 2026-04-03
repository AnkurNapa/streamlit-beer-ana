"""
Master Brewer - Comprehensive Streamlit App
All features from Beer Analytics integrated
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from data_loader_enhanced import EnhancedDataLoader

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Master Brewer - Complete Beer Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Master Brewer - Complete Beer Brewing & Analytics Tool"},
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
    .metric-card {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #FF6B35;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== INITIALIZATION ====================
if "page" not in st.session_state:
    st.session_state.page = "Home"

loader = EnhancedDataLoader()

# ==================== SIDEBAR NAVIGATION ====================
st.sidebar.markdown("# 🍺 **MASTER BREWER**")
st.sidebar.markdown("### The Complete Beer Analytics Platform")
st.sidebar.markdown("---")

# Navigation categories
st.sidebar.markdown("### 🏠 **HOME**")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "Home"

st.sidebar.markdown("### 📚 **EXPLORE DATA**")
if st.sidebar.button("🔍 Recipe Search & Filter", use_container_width=True):
    st.session_state.page = "Recipe Search"
if st.sidebar.button("🍻 Beer Styles Guide", use_container_width=True):
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
if st.sidebar.button("📊 Flavor Wheel", use_container_width=True):
    st.session_state.page = "Flavor Wheel"
if st.sidebar.button("💧 IBU/ABV/Color", use_container_width=True):
    st.session_state.page = "IBU Calculator"
if st.sidebar.button("🤝 Hop Pairings", use_container_width=True):
    st.session_state.page = "Pairings"

st.sidebar.markdown("### 📈 **ANALYTICS**")
if st.sidebar.button("📊 Community Statistics", use_container_width=True):
    st.session_state.page = "Analytics"
if st.sidebar.button("🔥 Trending", use_container_width=True):
    st.session_state.page = "Trending"
if st.sidebar.button("🏆 Popular Items", use_container_width=True):
    st.session_state.page = "Popular"

st.sidebar.markdown("### 🧪 **BUILD**")
if st.sidebar.button("📋 Recipe Builder", use_container_width=True):
    st.session_state.page = "Recipe Builder"

st.sidebar.markdown("---")

# Data status
if loader.has_data():
    st.sidebar.success("✅ Beer Analytics Data Loaded!")
else:
    st.sidebar.warning(
        """⚠️ Data not loaded. Run:
    ```
    python scraper_enhanced.py
    ```
    """
    )

st.sidebar.info("💡 Start with Home or Recipe Search to explore!")

# ==================== HOME PAGE ====================
if st.session_state.page == "Home":
    st.markdown(
        '<p class="main-title">🍺 Master Brewer</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">The Complete Beer Analytics & Brewing Platform</p>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="card-container"><h3>🔍 Search Recipes</h3></div>',
            unsafe_allow_html=True,
        )
        st.markdown("Search 1M+ real recipes with advanced filters")
        if st.button("👉 Search Now", key="home_search", use_container_width=True):
            st.session_state.page = "Recipe Search"
            st.rerun()

    with col2:
        st.markdown(
            '<div class="card-container"><h3>📊 Analytics</h3></div>',
            unsafe_allow_html=True,
        )
        st.markdown("Explore community brewing statistics & trends")
        if st.button("👉 View Analytics", key="home_analytics", use_container_width=True):
            st.session_state.page = "Analytics"
            st.rerun()

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="card-container"><h3>🧪 Build Recipe</h3></div>',
            unsafe_allow_html=True,
        )
        st.markdown("Create your perfect beer recipe step-by-step")
        if st.button("👉 Build Recipe", key="home_build", use_container_width=True):
            st.session_state.page = "Recipe Builder"
            st.rerun()

    with col2:
        st.markdown(
            '<div class="card-container"><h3>📚 Learn</h3></div>',
            unsafe_allow_html=True,
        )
        st.markdown("Explore beer styles, hops, yeasts & more")
        if st.button("👉 Explore Data", key="home_explore", use_container_width=True):
            st.session_state.page = "Beer Styles"
            st.rerun()

    st.markdown("---")

    # Quick stats
    st.markdown("### 📊 Quick Stats")
    stats = loader.get_recipe_statistics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Recipes", f"{stats.get('total_recipes', 0):,}")
    with col2:
        st.metric("Avg IBU", f"{stats.get('avg_ibu', 0):.1f}")
    with col3:
        st.metric("Avg ABV", f"{stats.get('avg_abv', 0):.2f}%")
    with col4:
        st.metric("Avg Color", f"{stats.get('avg_color', 0):.1f} SRM")

    st.markdown("---")

    # Features
    st.markdown("### 🌟 Key Features")

    feature_col1, feature_col2, feature_col3 = st.columns(3)

    with feature_col1:
        st.markdown(
            """
            **📋 Recipe Search**
            - 1M+ recipes from the community
            - Advanced filtering
            - Ratings & difficulty
            - Detailed instructions
            """
        )

    with feature_col2:
        st.markdown(
            """
            **📚 Learning Library**
            - Beer styles with guidelines
            - Hop characteristics & pairings
            - Yeast profiles & best uses
            - Grain & fermentables info
            """
        )

    with feature_col3:
        st.markdown(
            """
            **📊 Analytics & Tools**
            - Community statistics
            - Trending items
            - IBU/ABV calculators
            - Flavor wheel
            - Recipe builder
            """
        )

# ==================== RECIPE SEARCH ====================
elif st.session_state.page == "Recipe Search":
    st.title("🔍 Recipe Search & Filtering")
    st.markdown("Search from 1M+ brewing recipes with advanced filters")

    st.markdown("### Filter Criteria")

    col1, col2, col3 = st.columns(3)

    with col1:
        search_style = st.text_input("🍻 Beer Style", placeholder="IPA, Stout, Lager...")
    with col2:
        search_category = st.text_input("📂 Category", placeholder="Pale Ale, Dark Beer...")
    with col3:
        search_difficulty = st.selectbox(
            "⭐ Difficulty",
            ["All", "Beginner", "Intermediate", "Advanced"],
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ibu_min = st.number_input("🔥 Min IBU", 0, 150, 0)
    with col2:
        ibu_max = st.number_input("🔥 Max IBU", 0, 150, 150)
    with col3:
        abv_min = st.number_input("🥃 Min ABV", 0.0, 15.0, 0.0, step=0.5)
    with col4:
        abv_max = st.number_input("🥃 Max ABV", 0.0, 15.0, 15.0, step=0.5)

    col1, col2 = st.columns(2)

    with col1:
        color_min = st.number_input("🎨 Min Color (SRM)", 0, 50, 0)
    with col2:
        color_max = st.number_input("🎨 Max Color (SRM)", 0, 50, 50)

    if st.button("🔎 Search Recipes", use_container_width=True):
        recipes = loader.filter_recipes(
            style=search_style if search_style else None,
            ibu_min=int(ibu_min),
            ibu_max=int(ibu_max),
            abv_min=float(abv_min),
            abv_max=float(abv_max),
            color_min=int(color_min),
            color_max=int(color_max),
        )

        if not recipes.empty:
            st.success(f"✅ Found {len(recipes)} recipes!")

            # Display table
            st.dataframe(recipes, use_container_width=True)

            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Count", len(recipes))
            with col2:
                if "ibu" in recipes.columns:
                    st.metric("Avg IBU", f"{recipes['ibu'].mean():.1f}")
            with col3:
                if "abv" in recipes.columns:
                    st.metric("Avg ABV", f"{recipes['abv'].mean():.2f}%")
            with col4:
                if "color" in recipes.columns:
                    st.metric("Avg Color", f"{recipes['color'].mean():.1f}")

            # Charts
            col1, col2 = st.columns(2)

            with col1:
                if "ibu" in recipes.columns:
                    fig = px.histogram(
                        recipes, x="ibu", nbins=30, title="IBU Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                if "abv" in recipes.columns:
                    fig = px.histogram(
                        recipes, x="abv", nbins=30, title="ABV Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No recipes found. Try different filters!")

# ==================== BEER STYLES ====================
elif st.session_state.page == "Beer Styles":
    st.title("🍻 Beer Styles Guide")
    st.markdown("Explore BJCP beer style guidelines")

    styles_df = loader.load_beer_styles()

    if styles_df is not None and not styles_df.empty:
        style_name = st.selectbox(
            "Select a Beer Style:",
            styles_df["name"].unique() if "name" in styles_df.columns else [],
        )

        if style_name:
            style_data = styles_df[
                styles_df["name"] == style_name
            ].iloc[0]

            st.markdown(f"## {style_name}")

            # Guidelines
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("IBU", f"{int(style_data['ibu_min'])}-{int(style_data['ibu_max'])}")
            with col2:
                st.metric("ABV", f"{style_data['abv_min']:.1f}-{style_data['abv_max']:.1f}%")
            with col3:
                st.metric("Color (SRM)", f"{int(style_data['color_min'])}-{int(style_data['color_max'])}")
            with col4:
                st.metric("OG", f"{style_data['og_min']:.3f}-{style_data['og_max']:.3f}")

            st.markdown("---")

            if "overall_impression" in style_data and pd.notna(style_data["overall_impression"]):
                st.markdown("### Overall Impression")
                st.write(style_data["overall_impression"])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🌿 Recommended Hops")
                if "recommended_hops" in style_data and style_data["recommended_hops"]:
                    for hop in style_data["recommended_hops"]:
                        st.write(f"• {hop}")

            with col2:
                st.markdown("### 🧬 Recommended Yeasts")
                if "recommended_yeasts" in style_data and style_data["recommended_yeasts"]:
                    for yeast in style_data["recommended_yeasts"]:
                        st.write(f"• {yeast}")

    else:
        st.info("Beer styles data not available. Run the scraper.")

# ==================== HOP LIBRARY ====================
elif st.session_state.page == "Hop Library":
    st.title("🌿 Hop Library")
    st.markdown("Explore hop varieties and characteristics")

    hops_df = loader.load_hops()

    if hops_df is not None and not hops_df.empty:
        hop_name = st.selectbox(
            "Select a Hop:",
            hops_df["name"].unique() if "name" in hops_df.columns else [],
        )

        if hop_name:
            hop_data = hops_df[hops_df["name"] == hop_name].iloc[0]

            st.markdown(f"## {hop_name}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Alpha Acids", f"{hop_data['alpha_acids']:.1f}%")
            with col2:
                st.metric("Beta Acids", f"{hop_data.get('beta_acids', 'N/A')}")
            with col3:
                st.metric("Origin", hop_data["origin"])
            with col4:
                st.metric("Type", hop_data["purpose"])

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 👃 Aroma")
                if "aroma" in hop_data and hop_data["aroma"]:
                    for aroma in hop_data["aroma"]:
                        st.write(f"• {aroma}")

            with col2:
                st.markdown("### 🍯 Flavor")
                if "flavor" in hop_data and hop_data["flavor"]:
                    for flavor in hop_data["flavor"]:
                        st.write(f"• {flavor}")

            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.info(f"""
                **Bittering (60 min)**
                {hop_data.get('bittering_oz', 'N/A')} oz
                """)

            with col2:
                st.info(f"""
                **Aroma (5-15 min)**
                {hop_data.get('aroma_oz', 'N/A')} oz
                """)

            with col3:
                st.info(f"""
                **Dry Hop**
                {hop_data.get('dry_hop_oz', 'N/A')} oz
                """)

            st.markdown("---")

            st.markdown("### 🤝 Pairs Well With")
            if "pairs_well_with" in hop_data and hop_data["pairs_well_with"]:
                for paired_hop in hop_data["pairs_well_with"]:
                    st.success(f"✓ {paired_hop}")

    else:
        st.info("Hop data not available. Run the scraper.")

# ==================== YEAST LIBRARY ====================
elif st.session_state.page == "Yeast Library":
    st.title("🧬 Yeast Library")
    st.markdown("Explore yeast strains and their characteristics")

    yeasts_df = loader.load_yeasts()

    if yeasts_df is not None and not yeasts_df.empty:
        yeast_name = st.selectbox(
            "Select a Yeast:",
            yeasts_df["name"].unique() if "name" in yeasts_df.columns else [],
        )

        if yeast_name:
            yeast_data = yeasts_df[yeasts_df["name"] == yeast_name].iloc[0]

            st.markdown(f"## {yeast_name}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Type", yeast_data["type"])
            with col2:
                temp_min = yeast_data.get("temperature_min", "N/A")
                temp_max = yeast_data.get("temperature_max", "N/A")
                st.metric("Temp Range", f"{temp_min}-{temp_max}°F")
            with col3:
                att_min = yeast_data.get("attenuation_min", "N/A")
                att_max = yeast_data.get("attenuation_max", "N/A")
                st.metric("Attenuation", f"{att_min}-{att_max}%")
            with col4:
                st.metric("Flocculation", yeast_data.get("flocculation", "N/A"))

            st.markdown("---")

            st.markdown("### 🌡️ Flavor Profile")
            if "flavor_profile" in yeast_data and yeast_data["flavor_profile"]:
                st.write(yeast_data["flavor_profile"])

            st.markdown("---")

            st.markdown("### 🍻 Best For")
            if "best_for" in yeast_data and yeast_data["best_for"]:
                for style in yeast_data["best_for"]:
                    st.write(f"• {style}")

    else:
        st.info("Yeast data not available. Run the scraper.")

# ==================== FERMENTABLES ====================
elif st.session_state.page == "Fermentables":
    st.title("🌾 Fermentables Library")
    st.markdown("Explore grains, malts, and other fermentables")

    fermentables_df = loader.load_fermentables()

    if fermentables_df is not None and not fermentables_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            grain_type = st.multiselect(
                "Filter by Type:",
                fermentables_df["type"].unique()
                if "type" in fermentables_df.columns
                else [],
            )

        if grain_type:
            filtered = fermentables_df[fermentables_df["type"].isin(grain_type)]
        else:
            filtered = fermentables_df

        st.dataframe(filtered, use_container_width=True)

        st.markdown("---")

        # Top grains chart
        if "recipes" in filtered.columns:
            st.markdown("### 📈 Most Popular Grains")
            top_grains = filtered.nlargest(10, "recipes")
            fig = px.bar(
                top_grains,
                x="recipes",
                y="name",
                title="Most Used Grains by Recipe Count",
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Fermentables data not available. Run the scraper.")

# ==================== ADVANCED FILTERS ====================
elif st.session_state.page == "Advanced Filters":
    st.title("⚙️ Advanced Filtering Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["Recipes", "Hops", "Yeasts", "Fermentables"])

    with tab1:
        st.markdown("### Advanced Recipe Filtering")

        col1, col2 = st.columns(2)

        with col1:
            style = st.text_input("Beer Style")
            ibu_min, ibu_max = st.slider("IBU Range", 0, 150, (20, 80))
            abv_min, abv_max = st.slider("ABV Range", 0.0, 15.0, (4.0, 6.0))

        with col2:
            color_min, color_max = st.slider("Color (SRM) Range", 0, 50, (5, 15))
            og_min, og_max = st.slider("OG Range", 1.0, 1.2, (1.04, 1.08), step=0.01)

        if st.button("Apply Filters", key="recipe_filter"):
            recipes = loader.filter_recipes(
                style=style if style else None,
                ibu_min=ibu_min,
                ibu_max=ibu_max,
                abv_min=abv_min,
                abv_max=abv_max,
                color_min=color_min,
                color_max=color_max,
                og_min=og_min,
                og_max=og_max,
            )

            if not recipes.empty:
                st.success(f"Found {len(recipes)} recipes")
                st.dataframe(recipes, use_container_width=True)
            else:
                st.warning("No recipes match your criteria")

    with tab2:
        st.markdown("### Hop Filtering")

        col1, col2 = st.columns(2)

        with col1:
            aa_min, aa_max = st.slider("Alpha Acids %", 0.0, 20.0, (0.0, 15.0))
            origin = st.text_input("Origin")

        with col2:
            purpose = st.selectbox("Purpose", ["All", "Bittering", "Aroma", "Dual"])
            flavor = st.text_input("Flavor")

        if st.button("Apply Hop Filters", key="hop_filter"):
            hops = loader.filter_hops(
                alpha_acids_min=aa_min,
                alpha_acids_max=aa_max,
                origin=origin if origin else None,
                purpose=purpose if purpose != "All" else None,
                flavor=flavor if flavor else None,
            )

            if not hops.empty:
                st.success(f"Found {len(hops)} hops")
                st.dataframe(hops, use_container_width=True)
            else:
                st.warning("No hops match your criteria")

    with tab3:
        st.markdown("### Yeast Filtering")

        col1, col2 = st.columns(2)

        with col1:
            yeast_type = st.selectbox("Type", ["All", "Ale", "Lager", "Hybrid"])
            temp_min, temp_max = st.slider("Temp Range (°F)", 50, 80, (62, 68))

        with col2:
            att_min, att_max = st.slider("Attenuation %", 0.0, 100.0, (70.0, 80.0))
            flocculation = st.selectbox(
                "Flocculation", ["All", "Low", "Medium", "High"]
            )

        if st.button("Apply Yeast Filters", key="yeast_filter"):
            yeasts = loader.filter_yeasts(
                yeast_type=yeast_type if yeast_type != "All" else None,
                temp_min=temp_min,
                temp_max=temp_max,
                attenuation_min=att_min,
                flocculation=flocculation if flocculation != "All" else None,
            )

            if not yeasts.empty:
                st.success(f"Found {len(yeasts)} yeasts")
                st.dataframe(yeasts, use_container_width=True)
            else:
                st.warning("No yeasts match your criteria")

    with tab4:
        st.markdown("### Fermentables Filtering")

        col1, col2 = st.columns(2)

        with col1:
            grain_type = st.text_input("Grain Type")
            color_min, color_max = st.slider("Color (SRM) Range", 0, 50, (0, 50))

        with col2:
            ppg_min = st.number_input("Min PPG", 0.0, 50.0, 0.0)

        if st.button("Apply Fermentables Filters", key="ferm_filter"):
            fermentables = loader.filter_fermentables(
                grain_type=grain_type if grain_type else None,
                color_min=color_min,
                color_max=color_max,
                ppg_min=ppg_min if ppg_min > 0 else None,
            )

            if not fermentables.empty:
                st.success(f"Found {len(fermentables)} fermentables")
                st.dataframe(fermentables, use_container_width=True)
            else:
                st.warning("No fermentables match your criteria")

# ==================== ANALYTICS ====================
elif st.session_state.page == "Analytics":
    st.title("📊 Community Statistics")
    st.markdown("Analytics from the Beer Analytics community database")

    stats = loader.get_recipe_statistics()
    style_stats = loader.get_style_statistics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Recipes", f"{stats.get('total_recipes', 0):,}")
    with col2:
        st.metric("Avg IBU", f"{stats.get('avg_ibu', 0):.1f}")
    with col3:
        st.metric("Avg ABV", f"{stats.get('avg_abv', 0):.2f}%")
    with col4:
        st.metric("Avg Color", f"{stats.get('avg_color', 0):.1f} SRM")

    st.markdown("---")

    recipes = loader.load_recipes()

    if recipes is not None and not recipes.empty:
        col1, col2 = st.columns(2)

        with col1:
            if "ibu" in recipes.columns:
                fig = px.histogram(
                    recipes, x="ibu", nbins=50, title="IBU Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if "abv" in recipes.columns:
                fig = px.histogram(
                    recipes, x="abv", nbins=50, title="ABV Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            if "color" in recipes.columns:
                fig = px.histogram(
                    recipes, x="color", nbins=50, title="Color (SRM) Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if "og" in recipes.columns:
                fig = px.histogram(
                    recipes, x="og", nbins=50, title="Original Gravity Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        if style_stats:
            st.markdown("### Statistics by Style")
            style_df = pd.DataFrame(style_stats).T
            st.dataframe(style_df, use_container_width=True)

# ==================== TRENDING ====================
elif st.session_state.page == "Trending":
    st.title("🔥 Trending")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🌿 Popular Hops")
        popular_hops = loader.get_popular_hops(10)
        if not popular_hops.empty:
            for i, (idx, hop) in enumerate(popular_hops.iterrows(), 1):
                st.write(f"{i}. {hop['name']}")

    with col2:
        st.markdown("### 🧬 Popular Yeasts")
        popular_yeasts = loader.get_popular_yeasts(10)
        if not popular_yeasts.empty:
            for i, (idx, yeast) in enumerate(popular_yeasts.iterrows(), 1):
                st.write(f"{i}. {yeast['name']}")

    with col3:
        st.markdown("### 🌾 Popular Grains")
        popular_grains = loader.get_popular_grains(10)
        if not popular_grains.empty:
            for i, (idx, grain) in enumerate(popular_grains.iterrows(), 1):
                st.write(f"{i}. {grain['name']}")

# ==================== POPULAR ====================
elif st.session_state.page == "Popular":
    st.title("🏆 Most Popular Items")

    tab1, tab2, tab3 = st.tabs(["Hops", "Yeasts", "Grains"])

    with tab1:
        st.markdown("### 🌿 Most Popular Hops")
        hops = loader.get_popular_hops(20)
        if not hops.empty:
            fig = px.bar(hops, x="recipes", y="name", title="Hops by Recipe Count")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 🧬 Most Popular Yeasts")
        yeasts = loader.get_popular_yeasts(20)
        if not yeasts.empty:
            fig = px.bar(
                yeasts, x="recipes", y="name", title="Yeasts by Recipe Count"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### 🌾 Most Popular Grains")
        grains = loader.get_popular_grains(20)
        if not grains.empty:
            fig = px.bar(grains, x="recipes", y="name", title="Grains by Recipe Count")
            st.plotly_chart(fig, use_container_width=True)

# ==================== FLAVOR WHEEL ====================
elif st.session_state.page == "Flavor Wheel":
    st.title("🎨 Flavor Wheel")

    selected_hops = st.multiselect(
        "Select hops to compare:",
        loader.load_hops()["name"].unique() if loader.load_hops() is not None else [],
        default=["Citra", "Cascade"] if loader.load_hops() is not None else []
    )

    if selected_hops:
        st.info("Flavor wheel comparison feature coming soon!")

# ==================== IBU CALCULATOR ====================
elif st.session_state.page == "IBU Calculator":
    st.title("💧 IBU / ABV / Color Calculator")

    tab1, tab2, tab3 = st.tabs(["IBU Calculator", "ABV Calculator", "Color Chart"])

    with tab1:
        st.markdown("### IBU Calculation")

        hops = loader.load_hops()
        if hops is not None and not hops.empty:
            selected_hop = st.selectbox("Select Hop:", hops["name"].unique())

            if selected_hop:
                hop_data = hops[hops["name"] == selected_hop].iloc[0]

                col1, col2 = st.columns(2)

                with col1:
                    amount_oz = st.number_input("Amount (oz)", 0.5, 3.0, 1.0)
                with col2:
                    boil_time = st.slider("Boil Time (min)", 0, 90, 60)

                # Simple IBU calculation
                util_factors = {
                    0: 0.05, 5: 0.10, 10: 0.15, 15: 0.20, 20: 0.30,
                    30: 0.40, 45: 0.50, 60: 0.65, 75: 0.70, 90: 0.72,
                }

                closest_time = min(util_factors.keys(), key=lambda x: abs(x - boil_time))
                util_factor = util_factors[closest_time]

                ibu = amount_oz * float(hop_data["alpha_acids"]) * util_factor

                st.success(f"**Estimated IBU: {ibu:.1f}**")

    with tab2:
        st.markdown("### ABV Calculator")
        og = st.number_input("Original Gravity (OG)", 1.0, 1.2, 1.05, step=0.001)
        fg = st.number_input("Final Gravity (FG)", 0.98, 1.05, 1.01, step=0.001)

        abv = (og - fg) * 131.25
        st.success(f"**ABV: {abv:.2f}%**")

    with tab3:
        st.markdown("### Color (SRM) Chart")
        color_values = list(range(0, 51, 5))
        colors = ["#FFE699", "#F1D04A", "#D4A017", "#8B6F47", "#3D2817", "#000000"]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=color_values[:len(colors)],
                    y=[1] * len(colors),
                    marker=dict(color=colors),
                    showlegend=False,
                )
            ]
        )
        fig.update_layout(title="SRM Color Scale", xaxis_title="SRM", yaxis_title="", height=300)
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAIRINGS ====================
elif st.session_state.page == "Pairings":
    st.title("🤝 Hop Pairings")

    hops = loader.load_hops()

    if hops is not None and not hops.empty:
        primary_hop = st.selectbox("Select a Hop:", hops["name"].unique())

        if primary_hop:
            pairings = loader.get_hop_pairings(primary_hop)

            st.markdown(f"### {primary_hop} pairs well with:")

            if pairings:
                cols = st.columns(len(pairings))
                for i, paired_hop in enumerate(pairings):
                    with cols[i]:
                        st.success(f"✓ {paired_hop}")
            else:
                st.info("No pairing data available")

# ==================== RECIPE BUILDER ====================
elif st.session_state.page == "Recipe Builder":
    st.title("📋 Recipe Builder")

    st.markdown("### Step 1: Choose Your Beer Style")

    styles = loader.load_beer_styles()

    if styles is not None and not styles.empty:
        selected_style = st.selectbox("Beer Style:", styles["name"].unique() if "name" in styles.columns else [])

        if selected_style:
            style_guidelines = loader.get_style_guidelines(selected_style)

            if style_guidelines:
                st.markdown("---")
                st.markdown("### Step 2: Recipe Parameters")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    batch_size = st.number_input("Batch Size (gal)", 1, 100, 5)
                with col2:
                    target_ibu = st.slider(
                        "Target IBU",
                        int(style_guidelines["ibu_min"]),
                        int(style_guidelines["ibu_max"]),
                        int((style_guidelines["ibu_min"] + style_guidelines["ibu_max"]) / 2),
                    )
                with col3:
                    target_abv = st.slider(
                        "Target ABV",
                        style_guidelines["abv_min"],
                        style_guidelines["abv_max"],
                        (style_guidelines["abv_min"] + style_guidelines["abv_max"]) / 2,
                    )
                with col4:
                    target_color = st.slider(
                        "Target Color (SRM)",
                        int(style_guidelines["color_min"]),
                        int(style_guidelines["color_max"]),
                        int((style_guidelines["color_min"] + style_guidelines["color_max"]) / 2),
                    )

                st.markdown("---")
                st.markdown("### Step 3: Select Ingredients")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Bittering Hops**")
                    bittering_hops = st.multiselect(
                        "Choose hops (60 min):",
                        loader.get_recommended_hops(selected_style)
                        if loader.get_recommended_hops(selected_style)
                        else [],
                        key="bittering",
                    )

                with col2:
                    st.markdown("**Aroma Hops**")
                    aroma_hops = st.multiselect(
                        "Choose hops (5-15 min):",
                        loader.get_recommended_hops(selected_style)
                        if loader.get_recommended_hops(selected_style)
                        else [],
                        key="aroma",
                    )

                with col3:
                    st.markdown("**Yeast**")
                    yeast = st.selectbox(
                        "Choose yeast:",
                        loader.get_recommended_yeasts(selected_style)
                        if loader.get_recommended_yeasts(selected_style)
                        else [],
                    )

                if st.button("📋 Generate Recipe", use_container_width=True):
                    st.success("✅ Recipe Generated!")

                    st.markdown(f"""
                    ## {selected_style}

                    **Batch Size:** {batch_size} gallons
                    **Target IBU:** {target_ibu}
                    **Target ABV:** {target_abv:.2f}%
                    **Target Color:** {target_color} SRM

                    ### Ingredients

                    **Bittering Hops (60 min):**
                    {', '.join(bittering_hops) if bittering_hops else 'None'}

                    **Aroma Hops (5-15 min):**
                    {', '.join(aroma_hops) if aroma_hops else 'None'}

                    **Yeast:**
                    {yeast if yeast else 'None'}

                    ### Style Guidelines

                    {style_guidelines.get('overall_impression', 'N/A')}
                    """)

if __name__ == "__main__":
    pass
