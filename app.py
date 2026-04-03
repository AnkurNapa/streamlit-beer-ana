import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from data_loader import DataLoader

# Set page config
st.set_page_config(
    page_title="Master Brewer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Master Brewer - Your AI Beer Assistant"}
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.3em;
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
    </style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_beer_styles():
    """Load BJCP beer style data"""
    csv_path = Path("data/bjcp-style-data/csv/beer-vital-statistics-2008.csv")
    df = pd.read_csv(csv_path)
    return df

@st.cache_data
def load_hop_database():
    """Create a hop flavor profile database with pairing info"""
    hops = {
        'Cascade': {'AA': 5.5, 'Beta': 5.0, 'flavor': ['citrus', 'floral', 'spicy'], 'aroma': ['citrus', 'grapefruit'], 'origin': 'USA', 'alpha_acids': 5.5, 'type': 'Aroma', 'pairs_with': ['Centennial', 'Amarillo'], 'bittering_oz': (0.75, 1.25), 'aroma_oz': (0.75, 1.5), 'dry_hop_oz': (1.0, 2.0)},
        'Citra': {'AA': 12.5, 'Beta': 3.5, 'flavor': ['citrus', 'tropical', 'pine'], 'aroma': ['grapefruit', 'lemon'], 'origin': 'USA', 'alpha_acids': 12.5, 'type': 'Bittering', 'pairs_with': ['Mosaic', 'Amarillo'], 'bittering_oz': (1.0, 1.5), 'aroma_oz': (0.5, 1.0), 'dry_hop_oz': (1.0, 2.0)},
        'Mosaic': {'AA': 11.5, 'Beta': 2.0, 'flavor': ['berry', 'herbal', 'citrus'], 'aroma': ['blueberry', 'pine'], 'origin': 'USA', 'alpha_acids': 11.5, 'type': 'Bittering/Aroma', 'pairs_with': ['Citra', 'Galaxy'], 'bittering_oz': (0.75, 1.25), 'aroma_oz': (0.5, 1.0), 'dry_hop_oz': (1.0, 2.0)},
        'Simcoe': {'AA': 13, 'Beta': 4.0, 'flavor': ['pine', 'citrus', 'herbal'], 'aroma': ['pine', 'earthy'], 'origin': 'USA', 'alpha_acids': 13, 'type': 'Bittering', 'pairs_with': ['Centennial', 'Citra'], 'bittering_oz': (1.0, 1.5), 'aroma_oz': (0.5, 1.0), 'dry_hop_oz': (0.75, 1.5)},
        'Amarillo': {'AA': 9.2, 'Beta': 2.7, 'flavor': ['citrus', 'floral'], 'aroma': ['orange', 'lemon'], 'origin': 'USA', 'alpha_acids': 9.2, 'type': 'Bittering/Aroma', 'pairs_with': ['Cascade', 'Citra'], 'bittering_oz': (0.75, 1.25), 'aroma_oz': (0.75, 1.25), 'dry_hop_oz': (0.75, 1.5)},
        'Saaz': {'AA': 3.0, 'Beta': 3.5, 'flavor': ['herbal', 'spicy', 'earthy'], 'aroma': ['herbal', 'noble'], 'origin': 'Czech', 'alpha_acids': 3.0, 'type': 'Aroma', 'pairs_with': ['Hallertau'], 'bittering_oz': (0.5, 1.0), 'aroma_oz': (0.5, 1.0), 'dry_hop_oz': (0.5, 1.0)},
        'Hallertau': {'AA': 4.7, 'Beta': 4.4, 'flavor': ['herbal', 'floral', 'earthy'], 'aroma': ['herbal', 'spicy'], 'origin': 'Germany', 'alpha_acids': 4.7, 'type': 'Aroma', 'pairs_with': ['Saaz'], 'bittering_oz': (0.75, 1.25), 'aroma_oz': (0.75, 1.5), 'dry_hop_oz': (0.5, 1.0)},
        'Fuggle': {'AA': 4.5, 'Beta': 1.9, 'flavor': ['earthy', 'herbal', 'woody'], 'aroma': ['earthy', 'tobacco'], 'origin': 'UK', 'alpha_acids': 4.5, 'type': 'Aroma', 'pairs_with': ['Goldings'], 'bittering_oz': (0.75, 1.25), 'aroma_oz': (0.75, 1.5), 'dry_hop_oz': (0.5, 1.0)},
        'Galaxy': {'AA': 13.5, 'Beta': 3.5, 'flavor': ['passionfruit', 'berry', 'citrus'], 'aroma': ['passionfruit', 'stone fruit'], 'origin': 'Australia', 'alpha_acids': 13.5, 'type': 'Bittering', 'pairs_with': ['Mosaic', 'Nelson Sauvin'], 'bittering_oz': (1.0, 1.5), 'aroma_oz': (0.5, 1.0), 'dry_hop_oz': (1.0, 2.0)},
        'Nelson Sauvin': {'AA': 11.5, 'Beta': 9.0, 'flavor': ['white wine', 'tropical', 'berry'], 'aroma': ['white wine', 'sauvignon'], 'origin': 'NZ', 'alpha_acids': 11.5, 'type': 'Aroma', 'pairs_with': ['Galaxy'], 'bittering_oz': (0.75, 1.25), 'aroma_oz': (0.75, 1.5), 'dry_hop_oz': (1.0, 2.0)},
        'Columbus': {'AA': 15, 'Beta': 5.5, 'flavor': ['woodsy', 'earthy', 'spicy'], 'aroma': ['herbal', 'woodsy'], 'origin': 'USA', 'alpha_acids': 15, 'type': 'Bittering', 'pairs_with': ['Simcoe'], 'bittering_oz': (1.0, 1.5), 'aroma_oz': (0.5, 1.0), 'dry_hop_oz': (0.5, 1.0)},
        'Centennial': {'AA': 9.5, 'Beta': 4.5, 'flavor': ['floral', 'citrus', 'herbal'], 'aroma': ['citrus', 'spicy'], 'origin': 'USA', 'alpha_acids': 9.5, 'type': 'Bittering/Aroma', 'pairs_with': ['Cascade', 'Saaz'], 'bittering_oz': (1.0, 1.5), 'aroma_oz': (0.5, 1.0), 'dry_hop_oz': (0.5, 1.5)},
        'Goldings': {'AA': 5.0, 'Beta': 2.0, 'flavor': ['herbal', 'earthy', 'spicy'], 'aroma': ['herbal', 'floral'], 'origin': 'UK', 'alpha_acids': 5.0, 'type': 'Aroma', 'pairs_with': ['Fuggle'], 'bittering_oz': (0.75, 1.25), 'aroma_oz': (0.75, 1.5), 'dry_hop_oz': (0.5, 1.0)},
    }
    return pd.DataFrame.from_dict(hops, orient='index')

@st.cache_data
def get_popular_hops():
    """Get most popular hops for quick access"""
    return ['Citra', 'Cascade', 'Mosaic', 'Simcoe']

# ==================== HELPER FUNCTIONS ====================
def create_flavor_wheel(flavors):
    """Create a flavor wheel spider chart"""
    flavor_categories = {
        'Citrus': 0, 'Floral': 0, 'Herbal': 0, 'Earthy': 0,
        'Pine': 0, 'Spicy': 0, 'Berry': 0, 'Tropical': 0
    }
    for flavor in flavors:
        for category in flavor_categories:
            if category.lower() in flavor.lower():
                flavor_categories[category] += 1
    return flavor_categories

def create_spider_chart(flavor_profile):
    """Create interactive spider/radar chart"""
    categories = list(flavor_profile.keys())
    values = list(flavor_profile.values())
    fig = go.Figure(data=go.Scatterpolar(
        r=values, theta=categories, fill='toself', name='Flavor Profile'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(values) + 1])),
        title="Flavor Profile", height=500, showlegend=False
    )
    return fig

def display_hop_card(hop_name, hops_db):
    """Display a beautiful hop card"""
    hop_data = hops_db.loc[hop_name]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Alpha Acids", f"{hop_data['alpha_acids']:.1f}%")
    with col2:
        st.metric("Type", hop_data['type'])
    with col3:
        st.metric("Origin", hop_data['origin'])
    with col4:
        st.metric("Beta Acids", f"{hop_data['Beta']:.1f}%")

    # Flavor and Aroma
    col1, col2 = st.columns(2)
    with col1:
        st.write("**🌸 Flavors:**")
        for f in hop_data['flavor']:
            st.write(f"  • {f.title()}")
    with col2:
        st.write("**👃 Aroma:**")
        for a in hop_data['aroma']:
            st.write(f"  • {a.title()}")

    return hop_data

# ==================== MAIN APP ====================
def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    # Sidebar Navigation with custom styling
    st.sidebar.markdown("# 🍺 **MASTER BREWER**")
    st.sidebar.markdown("---")

    st.sidebar.markdown("### 📚 **QUICK START**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'Home'
    with col2:
        if st.button("🎯 Quick Find", use_container_width=True):
            st.session_state.page = 'Quick Finder'

    st.sidebar.markdown("### 📖 **EXPLORE**")
    if st.sidebar.button("🌿 Hop Library", use_container_width=True):
        st.session_state.page = 'Hop Library'
    if st.sidebar.button("🍻 Beer Styles", use_container_width=True):
        st.session_state.page = 'Beer Styles'

    st.sidebar.markdown("### 🔧 **TOOLS**")
    if st.sidebar.button("🤝 Hop Pairings", use_container_width=True):
        st.session_state.page = 'Pairings'
    if st.sidebar.button("💧 Dosage & IBU", use_container_width=True):
        st.session_state.page = 'Dosage'
    if st.sidebar.button("🎨 Flavor Wheel", use_container_width=True):
        st.session_state.page = 'Flavors'

    st.sidebar.markdown("### 🧪 **BUILD**")
    if st.sidebar.button("📋 Build Recipe", use_container_width=True):
        st.session_state.page = 'Recipe'

    st.sidebar.markdown("### 📊 **ANALYTICS** (Beer Analytics)")
    if st.sidebar.button("🔍 Recipe Search", use_container_width=True):
        st.session_state.page = 'Recipe Search'
    if st.sidebar.button("📈 Trending", use_container_width=True):
        st.session_state.page = 'Trends'
    if st.sidebar.button("🧬 Yeasts", use_container_width=True):
        st.session_state.page = 'Yeasts'
    if st.sidebar.button("🌾 Fermentables", use_container_width=True):
        st.session_state.page = 'Fermentables'
    if st.sidebar.button("📉 Community Stats", use_container_width=True):
        st.session_state.page = 'Analytics'

    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip:** Start with Quick Find or Home to learn how to use this tool!")

    # Check for scraped data
    loader = DataLoader()
    if loader.has_scraped_data():
        st.sidebar.success("✅ Beer Analytics data loaded!")
    else:
        st.sidebar.warning("⚠️ Run scraper_firecrawl.py to load real data. See FIRECRAWL_SETUP.md")

    # Load data
    hops_db = load_hop_database()
    beer_styles = load_beer_styles()
    loader = DataLoader()  # Initialize data loader for Beer Analytics data

    # ==================== HOME PAGE ====================
    if st.session_state.page == 'Home':
        st.markdown('<p class="main-title">🍺 Master Brewer</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Your AI-Powered Beer Recipe & Hop Assistant</p>', unsafe_allow_html=True)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card-container"><h3>🎯 I Want to Find Hops</h3></div>', unsafe_allow_html=True)
            st.markdown("Know what beer you want? Let's find the perfect hops!")
            if st.button("👉 Quick Hop Finder", key="home_quick", use_container_width=True):
                st.session_state.page = 'Quick Finder'
                st.rerun()

        with col2:
            st.markdown('<div class="card-container"><h3>🧪 I Want to Build a Recipe</h3></div>', unsafe_allow_html=True)
            st.markdown("Let's create your beer step-by-step!")
            if st.button("👉 Recipe Builder", key="home_recipe", use_container_width=True):
                st.session_state.page = 'Recipe'
                st.rerun()

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card-container"><h3>📚 I Want to Learn Hops</h3></div>', unsafe_allow_html=True)
            st.markdown("Explore detailed hop profiles and characteristics!")
            if st.button("👉 Hop Library", key="home_library", use_container_width=True):
                st.session_state.page = 'Hop Library'
                st.rerun()

        with col2:
            st.markdown('<div class="card-container"><h3>🍻 I Want to Learn Beer Styles</h3></div>', unsafe_allow_html=True)
            st.markdown("Discover beer styles and their characteristics!")
            if st.button("👉 Beer Styles Guide", key="home_styles", use_container_width=True):
                st.session_state.page = 'Beer Styles'
                st.rerun()

        st.markdown("---")

        st.markdown("### 🌟 Popular Hops")
        popular = get_popular_hops()
        cols = st.columns(4)
        for i, hop in enumerate(popular):
            with cols[i]:
                hop_data = hops_db.loc[hop]
                st.info(f"""
                **{hop}**
                {hop_data['alpha_acids']:.1f}% AA
                {hop_data['type']}
                """)
                if st.button(f"View {hop}", key=f"home_hop_{hop}", use_container_width=True):
                    st.session_state.page = 'Hop Library'
                    st.session_state.selected_hop = hop
                    st.rerun()

        st.markdown("---")
        st.markdown("### ❓ How to Use")

        with st.expander("📖 Getting Started"):
            st.markdown("""
            **Master Brewer** helps you find hops, understand flavors, and build beer recipes.

            **3 Ways to Get Started:**
            1. **Quick Hop Finder** - Type in your beer style and we'll recommend hops
            2. **Beer Styles Guide** - Learn official style guidelines
            3. **Hop Library** - Explore detailed hop profiles
            """)

        with st.expander("🎯 What is IBU?"):
            st.markdown("""
            **IBU = International Bitterness Units**

            Measures how bitter a beer is from hops:
            - **0-30 IBU:** Mild (light ales, wheats)
            - **30-60 IBU:** Medium (pale ales, IPAs)
            - **60+ IBU:** Bold (double IPAs, imperial stouts)
            """)

        with st.expander("🌿 What are Alpha Acids?"):
            st.markdown("""
            **Alpha Acids = Hop Bitterness Potential**

            - **3-5% AA:** Aroma hops (gentle, flavorful)
            - **5-10% AA:** Dual-purpose (versatile)
            - **10%+ AA:** Bittering hops (intense)
            """)

    # ==================== QUICK FINDER ====================
    elif st.session_state.page == 'Quick Finder':
        st.title("🎯 Quick Hop Finder")
        st.markdown("Find perfect hops for your beer in seconds!")

        col1, col2, col3 = st.columns(3)

        with col1:
            ibu = st.slider("🔥 How bitter?", 0, 100, 50, help="IBU (International Bitterness Units)")
        with col2:
            abv = st.slider("🥃 How strong?", 2.0, 15.0, 5.5, help="ABV (Alcohol by Volume %)")
        with col3:
            style = st.text_input("🍻 Beer style", "IPA", help="E.g., IPA, Porter, Lager")

        if st.button("⚡ Find Hops Now!", use_container_width=True):
            # Get recommendations (simplified)
            recommendations = []
            for hop_name, hop_data in hops_db.iterrows():
                score = 0
                if ibu > 50 and hop_data['AA'] > 10:
                    score += 2
                elif ibu < 30 and hop_data['AA'] < 7:
                    score += 2
                if score > 0:
                    recommendations.append((hop_name, score, hop_data['AA']))

            recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

            if recommendations:
                st.success(f"✅ Found {len(recommendations)} compatible hops!")
                st.markdown("---")

                for hop_name, score, aa in recommendations:
                    with st.expander(f"🌿 {hop_name} ({aa:.1f}% AA) ⭐ {score}/5"):
                        display_hop_card(hop_name, hops_db)
                        if st.button(f"View Full Profile", key=f"quick_{hop_name}"):
                            st.session_state.page = 'Hop Library'
                            st.session_state.selected_hop = hop_name
                            st.rerun()
            else:
                st.warning("No matching hops found. Try different parameters!")

    # ==================== HOP LIBRARY ====================
    elif st.session_state.page == 'Hop Library':
        st.title("🌿 Hop Library")
        st.markdown("Explore detailed hop profiles and characteristics")

        selected_hop = st.selectbox("Select a hop:", hops_db.index, key="library_select")

        if selected_hop:
            st.markdown(f"## {selected_hop}")

            hop_data = display_hop_card(selected_hop, hops_db)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📊 Dosage Guidelines")
                st.info(f"""
                **Bittering (60 min):** {hop_data['bittering_oz'][0]:.2f} - {hop_data['bittering_oz'][1]:.2f} oz

                **Aroma (5-15 min):** {hop_data['aroma_oz'][0]:.2f} - {hop_data['aroma_oz'][1]:.2f} oz

                **Dry Hop:** {hop_data['dry_hop_oz'][0]:.2f} - {hop_data['dry_hop_oz'][1]:.2f} oz
                """)

            with col2:
                st.markdown("### 🤝 Pairs With")
                if hop_data['pairs_with']:
                    for paired in hop_data['pairs_with']:
                        st.success(f"✓ {paired}")

    # ==================== BEER STYLES ====================
    elif st.session_state.page == 'Beer Styles':
        st.title("🍻 Beer Styles Guide")

        col1, col2 = st.columns(2)

        with col1:
            category = st.selectbox("Category", beer_styles['Category'].unique())

        with col2:
            filtered = beer_styles[beer_styles['Category'] == category]
            style = st.selectbox("Beer Style", filtered['Sub-Category'].unique())

        style_data = beer_styles[beer_styles['Sub-Category'] == style].iloc[0]

        st.markdown(f"## {style}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔥 IBU Range", f"{int(style_data['IBU Min'])}-{int(style_data['IBU Max'])}")
        with col2:
            st.metric("🥃 ABV Range", f"{style_data['ABV Min']:.1f}-{style_data['ABV Max']:.1f}%")
        with col3:
            st.metric("🎨 Color (SRM)", f"{int(style_data['SRM Min'])}-{int(style_data['SRM Max'])}")
        with col4:
            st.metric("⚖️ Gravity (OG)", f"{style_data['OG Min']:.3f}-{style_data['OG Max']:.3f}")

    # ==================== PAIRINGS ====================
    elif st.session_state.page == 'Pairings':
        st.title("🤝 Hop Pairings")
        st.markdown("Discover which hops work great together!")

        primary = st.selectbox("Choose a hop:", hops_db.index)

        if primary:
            pairings = hops_db.loc[primary, 'pairs_with']
            st.markdown(f"### {primary} pairs well with:")

            cols = st.columns(len(pairings) if pairings else 1)
            for i, paired in enumerate(pairings if pairings else []):
                with cols[i]:
                    paired_data = hops_db.loc[paired]
                    st.success(f"""
                    **{paired}**
                    {paired_data['alpha_acids']:.1f}% AA
                    """)

    # ==================== DOSAGE ====================
    elif st.session_state.page == 'Dosage':
        st.title("💧 Dosage & IBU Calculator")

        hop = st.selectbox("Select hop:", hops_db.index)

        if hop:
            hop_data = hops_db.loc[hop]

            st.markdown(f"### {hop} Dosage")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Bittering (60 min)**\n{hop_data['bittering_oz'][0]:.2f} - {hop_data['bittering_oz'][1]:.2f} oz")
            with col2:
                st.info(f"**Aroma (5-15 min)**\n{hop_data['aroma_oz'][0]:.2f} - {hop_data['aroma_oz'][1]:.2f} oz")
            with col3:
                st.info(f"**Dry Hop**\n{hop_data['dry_hop_oz'][0]:.2f} - {hop_data['dry_hop_oz'][1]:.2f} oz")

            st.markdown("---")
            st.markdown("### 🧮 IBU Calculator")

            col1, col2 = st.columns(2)
            with col1:
                oz = st.slider("Amount (oz)", 0.5, 2.0, 1.0)
            with col2:
                minutes = st.slider("Boil time (min)", 10, 90, 60)

            # Simple IBU calc
            util = {10: 0.35, 15: 0.40, 20: 0.45, 30: 0.55, 45: 0.65, 60: 0.70, 90: 0.72}
            closest = min(util.keys(), key=lambda x: abs(x - minutes))
            ibu = oz * hop_data['alpha_acids'] * util[closest]

            st.success(f"**Estimated IBU: {ibu:.1f}**")

    # ==================== FLAVORS ====================
    elif st.session_state.page == 'Flavors':
        st.title("🎨 Flavor Wheel")

        selected_hops = st.multiselect("Select hops to compare:", hops_db.index, default=['Citra', 'Cascade'])

        if selected_hops:
            all_flavors = []
            for h in selected_hops:
                all_flavors.extend(hops_db.loc[h, 'flavor'])

            flavor_profile = create_flavor_wheel(all_flavors)
            fig = create_spider_chart(flavor_profile)
            st.plotly_chart(fig, use_container_width=True)

    # ==================== RECIPE SEARCH ====================
    elif st.session_state.page == 'Recipe Search':
        st.title("🔍 Recipe Search")
        st.markdown("Search from 1M+ real brewing recipes from Beer Analytics")

        col1, col2, col3 = st.columns(3)

        with col1:
            search_style = st.text_input("🍻 Beer Style", placeholder="IPA, Porter, Lager...")
        with col2:
            search_ibu_min = st.number_input("🔥 Min IBU", 0, 120, 0)
            search_ibu_max = st.number_input("🔥 Max IBU", 0, 120, 120)
        with col3:
            search_abv_min = st.number_input("🥃 Min ABV", 0.0, 15.0, 0.0)
            search_abv_max = st.number_input("🥃 Max ABV", 0.0, 15.0, 15.0)

        if st.button("🔎 Search Recipes", use_container_width=True):
            recipe_results = loader.search_recipes(
                style=search_style if search_style else None,
                ibu_min=int(search_ibu_min),
                ibu_max=int(search_ibu_max),
                abv_min=float(search_abv_min),
                abv_max=float(search_abv_max),
            )

            if not recipe_results.empty:
                st.success(f"✅ Found {len(recipe_results)} recipes!")

                # Display as sortable table
                sort_col = st.selectbox(
                    "Sort by:",
                    ["name", "ibu", "abv", "color"] if "ibu" in recipe_results.columns else ["name"],
                )
                sorted_results = recipe_results.sort_values(
                    sort_col, ascending=sort_col != "name"
                )

                st.dataframe(sorted_results, use_container_width=True)

                # Display statistics
                if "ibu" in sorted_results.columns:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(
                            "Avg IBU",
                            f"{sorted_results['ibu'].mean():.1f}",
                        )
                    with col2:
                        st.metric(
                            "Avg ABV",
                            f"{sorted_results['abv'].mean():.2f}%",
                        )
                    with col3:
                        st.metric(
                            "Avg Color",
                            f"{sorted_results['color'].mean():.1f}",
                        )
                    with col4:
                        st.metric("Recipe Count", len(sorted_results))
            else:
                st.warning("No recipes found. Try different filters!")

    # ==================== TRENDS ====================
    elif st.session_state.page == 'Trends':
        st.title("📈 Trending")
        st.markdown("See what's trending in the beer brewing community")

        trends_data = loader.load_trends()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🌿 Trending Hops")
            trending_hops = trends_data.get("trending_hops", [])
            if trending_hops:
                for i, hop in enumerate(trending_hops[:10], 1):
                    st.write(f"{i}. {hop}")
            else:
                st.info("Load trends data using the scraper")

        with col2:
            st.markdown("### 🍻 Trending Styles")
            trending_styles = trends_data.get("trending_styles", [])
            if trending_styles:
                for i, style in enumerate(trending_styles[:10], 1):
                    st.write(f"{i}. {style}")
            else:
                st.info("Load trends data using the scraper")

        st.markdown("---")

        st.markdown("### 🔥 Popular Hop Combinations")
        popular_hops = loader.get_popular_hops(limit=5)
        if not popular_hops.empty:
            for idx, (hop_name, hop_data) in enumerate(popular_hops.iterrows(), 1):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{idx}. {hop_name}**")
                with col2:
                    if "alpha_acids" in hop_data and pd.notna(hop_data["alpha_acids"]):
                        st.metric("AA%", f"{hop_data['alpha_acids']:.1f}")
                with col3:
                    if "recipes" in hop_data and pd.notna(hop_data["recipes"]):
                        st.metric("Recipes", int(hop_data["recipes"]))

    # ==================== YEASTS ====================
    elif st.session_state.page == 'Yeasts':
        st.title("🧬 Yeast Library")
        st.markdown("Explore brewing yeast strains and their characteristics")

        yeasts_df = loader.load_yeasts()

        if yeasts_df is not None and not yeasts_df.empty:
            selected_yeast = st.selectbox("Select a yeast:", yeasts_df["name"].unique() if "name" in yeasts_df.columns else [])

            if selected_yeast:
                yeast_data = yeasts_df[yeasts_df["name"] == selected_yeast].iloc[0]

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Type",
                        yeast_data.get("type", "N/A"),
                    )
                with col2:
                    st.metric(
                        "Attenuation",
                        yeast_data.get("attenuation", "N/A"),
                    )
                with col3:
                    st.metric(
                        "Temp Range",
                        yeast_data.get("temperature_range", "N/A"),
                    )
                with col4:
                    if "recipes" in yeast_data:
                        st.metric("Recipes", int(yeast_data["recipes"]))

                st.markdown("---")
                st.markdown("### 🌡️ Flavor Profile")
                if "flavor_profile" in yeast_data:
                    st.write(yeast_data["flavor_profile"])

            st.markdown("---")
            st.markdown("### 📊 Popular Yeasts")
            popular_yeasts = loader.get_popular_yeasts(limit=10)
            if not popular_yeasts.empty:
                st.dataframe(popular_yeasts, use_container_width=True)
        else:
            st.info("Yeast data not available. Run the scraper to load data.")

    # ==================== FERMENTABLES ====================
    elif st.session_state.page == 'Fermentables':
        st.title("🌾 Fermentables Library")
        st.markdown("Explore grains, malts, and other fermentables")

        fermentables_df = loader.load_fermentables()

        if fermentables_df is not None and not fermentables_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                grain_type = st.multiselect(
                    "Filter by type:",
                    fermentables_df["type"].unique() if "type" in fermentables_df.columns else [],
                )

            if grain_type:
                filtered = fermentables_df[fermentables_df["type"].isin(grain_type)]
            else:
                filtered = fermentables_df

            st.dataframe(filtered, use_container_width=True)

            st.markdown("---")
            st.markdown("### 📈 Most Used Fermentables")
            if "recipes" in filtered.columns:
                top_grains = filtered.nlargest(10, "recipes")
                fig = px.bar(
                    top_grains,
                    x="recipes",
                    y="name",
                    title="Most Popular Grains by Recipe Count",
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Fermentables data not available. Run the scraper to load data.")

    # ==================== ANALYTICS ====================
    elif st.session_state.page == 'Analytics':
        st.title("📉 Community Statistics")
        st.markdown("Analytics from the Beer Analytics community database")

        col1, col2 = st.columns(2)

        hop_stats = loader.get_hop_stats()
        recipe_stats = loader.get_recipe_stats()

        with col1:
            st.markdown("### 🌿 Hop Statistics")
            if hop_stats:
                st.metric("Total Hops", hop_stats.get("total_hops", 0))
                st.metric("Avg Alpha Acids", f"{hop_stats.get('avg_alpha_acids', 0):.2f}%")
                st.metric("Avg Recipes per Hop", f"{hop_stats.get('avg_recipes', 0):.0f}")
            else:
                st.info("Data not available")

        with col2:
            st.markdown("### 📋 Recipe Statistics")
            if recipe_stats:
                st.metric("Total Recipes", recipe_stats.get("total_recipes", 0))
                st.metric("Avg IBU", f"{recipe_stats.get('avg_ibu', 0):.1f}")
                st.metric("Avg ABV", f"{recipe_stats.get('avg_abv', 0):.2f}%")
            else:
                st.info("Data not available")

        st.markdown("---")

        # Recipe distribution charts
        recipes_df = loader.load_recipes()
        if recipes_df is not None and not recipes_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                if "ibu" in recipes_df.columns:
                    fig = px.histogram(
                        recipes_df,
                        x="ibu",
                        nbins=50,
                        title="IBU Distribution",
                        labels={"ibu": "IBU", "count": "Count"},
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                if "abv" in recipes_df.columns:
                    fig = px.histogram(
                        recipes_df,
                        x="abv",
                        nbins=50,
                        title="ABV Distribution",
                        labels={"abv": "ABV %", "count": "Count"},
                    )
                    st.plotly_chart(fig, use_container_width=True)

    # ==================== RECIPE ====================
    elif st.session_state.page == 'Recipe':
        st.title("🧪 Build Your Beer Recipe")

        st.markdown("### Step 1️⃣: Choose Your Beer Style")

        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", beer_styles['Category'].unique(), key="recipe_cat")
        with col2:
            filtered = beer_styles[beer_styles['Category'] == category]
            style = st.selectbox("Style", filtered['Sub-Category'].unique(), key="recipe_style")

        style_data = beer_styles[beer_styles['Sub-Category'] == style].iloc[0]

        st.markdown("### Step 2️⃣: Set Recipe Parameters")

        col1, col2, col3 = st.columns(3)
        with col1:
            batch = st.number_input("Batch size (gal)", 1, 100, 5)
        with col2:
            abv = st.slider("ABV", float(style_data['ABV Min']), float(style_data['ABV Max']),
                            float((style_data['ABV Min'] + style_data['ABV Max']) / 2))
        with col3:
            ibu = st.slider("IBU", int(style_data['IBU Min']), int(style_data['IBU Max']),
                           int((style_data['IBU Min'] + style_data['IBU Max']) / 2))

        st.markdown("### Step 3️⃣: Choose Your Hops")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Bittering (60 min)**")
            bittering = st.multiselect("", hops_db.index, key="bit", max_selections=2)
        with col2:
            st.markdown("**Aroma (5-15 min)**")
            aroma = st.multiselect("", hops_db.index, key="aroma", max_selections=2)
        with col3:
            st.markdown("**Dry Hop**")
            dry = st.multiselect("", hops_db.index, key="dry", max_selections=2)

        if st.button("📋 Generate Recipe!", use_container_width=True):
            st.success("✅ Recipe Generated!")

            st.markdown(f"""
            ## {style}

            **Batch Size:** {batch} gallons
            **Target ABV:** {abv}%
            **Target IBU:** {ibu}

            ### Hop Schedule
            | Stage | Hops | Amount |
            |-------|------|--------|
            | Bittering | {', '.join(bittering) if bittering else 'None'} | 60 min |
            | Aroma | {', '.join(aroma) if aroma else 'None'} | 5-15 min |
            | Dry Hop | {', '.join(dry) if dry else 'None'} | Post-boil |
            """)

if __name__ == "__main__":
    main()
