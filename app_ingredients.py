"""
Master Brewer - Ingredients Tool
Complete ingredient library, combinations, water chemistry, and recipe builder
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from streaming_loader import StreamingDataLoader
import math

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Master Brewer - Ingredients",
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
.success {
    background-color: #d4edda;
    padding: 12px;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin: 10px 0;
}
.recipe-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #FF6B35;
    margin: 15px 0;
}
.check-good {
    color: #28a745;
    font-weight: bold;
}
.check-bad {
    color: #dc3545;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==================== CLASSIC MALT DATA ====================
CLASSIC_MALTS = pd.DataFrame({
    'name': ['Pilsner', 'Maris Otter', 'Munich Light', 'Vienna',
             'Pale Ale', 'Crystal 20L', 'Crystal 40L', 'Crystal 60L', 'Crystal 80L',
             'Chocolate', 'Black Patent', 'Roasted Barley', 'Flaked Oats', 'Wheat'],
    'type': ['Base', 'Base', 'Base', 'Base', 'Base',
             'Crystal', 'Crystal', 'Crystal', 'Crystal',
             'Roasted', 'Roasted', 'Roasted', 'Adjunct', 'Adjunct'],
    'color': [1.5, 3, 8, 4.5, 5.5, 20, 40, 60, 80, 350, 2000, 300, 2, 2],
    'ppg': [37, 38, 36, 35, 37, 33, 31, 30, 28, 24, 23, 25, 28, 37],
    'max_in_batch': [100, 100, 100, 100, 100, 20, 20, 15, 10, 10, 5, 10, 10, 40]
})

# ==================== WATER PROFILES ====================
WATER_PROFILES = {
    'Pilsen': {'ca': 52, 'mg': 5, 'na': 20, 'cl': 20, 'so4': 10, 'hco3': 196},
    'Dublin': {'ca': 76, 'mg': 5, 'na': 28, 'cl': 47, 'so4': 19, 'hco3': 319},
    'Burton': {'ca': 295, 'mg': 52, 'na': 8, 'cl': 15, 'so4': 607, 'hco3': 0},
    'London': {'ca': 61, 'mg': 12, 'na': 28, 'cl': 57, 'so4': 93, 'hco3': 160},
    'Munich': {'ca': 75, 'mg': 18, 'na': 9, 'cl': 14, 'so4': 43, 'hco3': 280},
    'Vienna': {'ca': 100, 'mg': 15, 'na': 12, 'cl': 20, 'so4': 70, 'hco3': 300},
    'Generic Soft': {'ca': 20, 'mg': 5, 'na': 20, 'cl': 20, 'so4': 10, 'hco3': 50},
    'Generic Hard': {'ca': 150, 'mg': 40, 'na': 50, 'cl': 100, 'so4': 200, 'hco3': 300},
}

# Mineral salt composition (ppm contribution per 1g per gallon)
MINERAL_ADDITIONS = {
    'CaSO4': {'ca': 61.5, 'so4': 147.4},
    'CaCl2': {'ca': 72.0, 'cl': 127.5},
    'MgSO4': {'mg': 26.1, 'so4': 103.0},
    'NaCl': {'na': 104.0, 'cl': 160.3},
    'NaHCO3': {'na': 76.7, 'hco3': 190.9},
    'CaCO3': {'ca': 105.9, 'hco3': 158.8},
}

# ==================== INITIALIZATION ====================
@st.cache_resource
def get_loader():
    return StreamingDataLoader()

loader = get_loader()

if "page" not in st.session_state:
    st.session_state.page = "home"

# ==================== CALCULATIONS ====================
def calculate_srm(malt_bill: Dict[str, float], batch_size_gal: float = 5) -> float:
    """Calculate SRM color from malt bill using Morey formula"""
    if not malt_bill or batch_size_gal <= 0:
        return 0

    mcu = 0
    for malt_name, weight_lb in malt_bill.items():
        malt = CLASSIC_MALTS[CLASSIC_MALTS['name'] == malt_name]
        if not malt.empty:
            color = malt.iloc[0]['color']
            mcu += (color * weight_lb) / batch_size_gal

    if mcu == 0:
        return 0
    return min(1.4922 * (mcu ** 0.6859), 90)

def calculate_ibu(hop_oz: float, alpha_acid_pct: float, boil_time: int, og: float) -> float:
    """Calculate IBU using simplified Tinseth formula"""
    if hop_oz <= 0 or alpha_acid_pct <= 0 or boil_time <= 0:
        return 0

    utilization = (1 - math.exp(-0.04 * boil_time)) / 4.15
    bigness_factor = 1.65 * (0.000125 ** (og - 1.0))
    ibu = (alpha_acid_pct / 100 * hop_oz * 7489 * utilization * bigness_factor) / 5.0
    return ibu

def calculate_abv(og: float, fg: float) -> float:
    """Calculate ABV from OG and FG"""
    if og < fg:
        return 0
    return (og - fg) * 131.25

def srm_to_hex(srm: float) -> str:
    """Convert SRM to approximate hex color"""
    # Simplified SRM to RGB conversion
    if srm < 2:
        return "#FFF8DC"
    elif srm < 5:
        return "#FFEB9C"
    elif srm < 10:
        return "#FFD700"
    elif srm < 20:
        return "#FF8C00"
    elif srm < 30:
        return "#DC6C3E"
    elif srm < 40:
        return "#8B4513"
    else:
        return "#1C1C1C"

# ==================== SIDEBAR ====================
st.sidebar.markdown("# 🍺 **MASTER BREWER**")
st.sidebar.markdown("### Ingredients Tool")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📚 **PAGES**")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "home"
if st.sidebar.button("🌾 Malt Library", use_container_width=True):
    st.session_state.page = "malts"
if st.sidebar.button("🔄 Malt Combinations", use_container_width=True):
    st.session_state.page = "combinations"
if st.sidebar.button("🌿 Hop Library", use_container_width=True):
    st.session_state.page = "hops"
if st.sidebar.button("🧬 Yeast Library", use_container_width=True):
    st.session_state.page = "yeasts"
if st.sidebar.button("💧 Water Chemistry", use_container_width=True):
    st.session_state.page = "water"
if st.sidebar.button("🔨 Recipe Builder", use_container_width=True):
    st.session_state.page = "builder"

st.sidebar.markdown("---")

# ==================== HOME PAGE ====================
def page_home():
    st.markdown('<h1 class="main-title">🍺 INGREDIENTS TOOL</h1>', unsafe_allow_html=True)
    st.markdown("### Master Your Beer Recipe Ingredients")

    st.markdown("""
    Complete toolkit for beer brewing ingredient exploration and recipe building:

    - 🌾 **Malt Library** — Browse classic brewing malts with color and yield
    - 🔄 **Malt Combinations** — Mix malts, calculate resulting color and style
    - 🌿 **Hop Library** — Full hop database with IBU calculator
    - 🧬 **Yeast Library** — Complete yeast profiles with ABV estimator
    - 💧 **Water Chemistry** — Build water profiles and calculate mineral additions
    - 🔨 **Recipe Builder** — Combine ingredients to build complete recipes
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Malts", len(CLASSIC_MALTS))
    with col2:
        st.metric("Water Profiles", len(WATER_PROFILES))
    with col3:
        st.metric("Mineral Salts", len(MINERAL_ADDITIONS))

# ==================== MALT LIBRARY PAGE ====================
def page_malts():
    st.markdown("# 🌾 Malt Library")

    col1, col2, col3 = st.columns(3)

    with col1:
        color_min = st.number_input("Min Color (Lovibond)", value=0, min_value=0, max_value=2000)
    with col2:
        color_max = st.number_input("Max Color (Lovibond)", value=2000, min_value=0, max_value=2000)
    with col3:
        malt_type = st.selectbox("Type", ["All"] + CLASSIC_MALTS['type'].unique().tolist())

    filtered = CLASSIC_MALTS[
        (CLASSIC_MALTS['color'] >= color_min) &
        (CLASSIC_MALTS['color'] <= color_max)
    ]

    if malt_type != "All":
        filtered = filtered[filtered['type'] == malt_type]

    filtered = filtered.sort_values('color')

    st.dataframe(filtered, use_container_width=True)

    # Color distribution chart
    st.markdown("### Color Distribution")
    color_counts = pd.cut(filtered['color'], bins=10).value_counts().sort_index()
    st.bar_chart(color_counts)

# ==================== MALT COMBINATIONS PAGE ====================
def page_combinations():
    st.markdown("# 🔄 Malt Combinations")
    st.markdown("Create custom malt bills and calculate resulting color and gravity")

    batch_size = st.number_input("Batch Size (gal)", value=5, min_value=1, max_value=100)

    st.markdown("### Select Malts & Weights")

    malts = st.multiselect(
        "Choose malts (up to 10)",
        CLASSIC_MALTS['name'].tolist(),
        max_selections=10
    )

    malt_weights = {}
    total_weight = 0

    if malts:
        cols = st.columns(len(malts))
        for i, malt in enumerate(malts):
            with cols[i]:
                weight = st.number_input(
                    f"{malt} (lb)",
                    value=1.0,
                    min_value=0.1,
                    max_value=50.0,
                    step=0.5,
                    key=f"weight_{malt}"
                )
                malt_weights[malt] = weight
                total_weight += weight

    if malt_weights:
        # Normalize to percentages
        st.markdown("### Malt Bill (normalized)")
        malt_pcts = {m: (w/total_weight)*100 for m, w in malt_weights.items()}

        malt_df = pd.DataFrame({
            'Malt': list(malt_pcts.keys()),
            'Weight (lb)': [malt_weights[m] for m in malt_pcts.keys()],
            'Percentage': [f"{pct:.1f}%" for pct in malt_pcts.values()]
        })
        st.dataframe(malt_df, use_container_width=True)

        # Calculate SRM
        srm = calculate_srm(malt_weights, batch_size)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            ### 🎨 Estimated Color
            **SRM: {srm:.1f}**
            """)
            color_hex = srm_to_hex(srm)
            st.markdown(f'<div style="background-color: {color_hex}; height: 80px; border-radius: 10px; border: 2px solid #333;"></div>', unsafe_allow_html=True)

        with col2:
            # Calculate gravity contribution
            total_ppg = 0
            for malt, weight in malt_weights.items():
                malt_data = CLASSIC_MALTS[CLASSIC_MALTS['name'] == malt]
                if not malt_data.empty:
                    ppg = malt_data.iloc[0]['ppg']
                    total_ppg += (ppg * weight)

            og = 1.0 + (total_ppg / (batch_size * 1000))
            st.markdown(f"""
            ### 📊 Estimated Gravity
            **OG: {og:.3f}**
            """)

# ==================== HOP LIBRARY PAGE ====================
def page_hops():
    st.markdown("# 🌿 Hop Library")

    hop_name = st.text_input("Search hops", placeholder="e.g., Cascade")

    if st.button("Load Hops", use_container_width=True):
        with st.spinner("Loading hops..."):
            hops_df = None
            for chunk in loader.stream_hops():
                if hops_df is None:
                    hops_df = chunk
                else:
                    hops_df = pd.concat([hops_df, chunk], ignore_index=True)

            if hops_df is not None and not hops_df.empty:
                if hop_name:
                    hops_df = hops_df[hops_df['name'].str.contains(hop_name, case=False, na=False)]

                st.dataframe(hops_df, use_container_width=True)

                # IBU Calculator
                st.markdown("### 📈 IBU Calculator")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    hop_oz = st.number_input("Hop Weight (oz)", value=1.0, min_value=0.1)
                with col2:
                    alpha = st.number_input("Alpha Acid %", value=10.0, min_value=0.0, max_value=20.0)
                with col3:
                    boil_time = st.number_input("Boil Time (min)", value=60, min_value=0, max_value=120)
                with col4:
                    og = st.number_input("OG", value=1.050, min_value=1.0, max_value=1.120)

                ibu = calculate_ibu(hop_oz, alpha, boil_time, og)
                st.metric("Estimated IBU", f"{ibu:.1f}")

# ==================== YEAST LIBRARY PAGE ====================
def page_yeasts():
    st.markdown("# 🧬 Yeast Library")

    yeast_type = st.text_input("Search yeasts", placeholder="e.g., Ale")

    if st.button("Load Yeasts", use_container_width=True):
        with st.spinner("Loading yeasts..."):
            yeasts_df = None
            for chunk in loader.stream_yeasts(yeast_type if yeast_type else None):
                if yeasts_df is None:
                    yeasts_df = chunk
                else:
                    yeasts_df = pd.concat([yeasts_df, chunk], ignore_index=True)

            if yeasts_df is not None and not yeasts_df.empty:
                st.dataframe(yeasts_df, use_container_width=True)

                # ABV Calculator
                st.markdown("### 🍻 ABV Calculator")
                col1, col2, col3 = st.columns(3)

                with col1:
                    og = st.number_input("OG", value=1.050, min_value=1.0, max_value=1.120, key="yeast_og")
                with col2:
                    attenuation = st.slider("Attenuation %", min_value=50, max_value=95, value=75)
                with col3:
                    st.empty()

                fg = og - ((og - 1.0) * (attenuation / 100))
                abv = calculate_abv(og, fg)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("FG", f"{fg:.3f}")
                with col2:
                    st.metric("ABV", f"{abv:.2f}%")
                with col3:
                    st.metric("Attenuation", f"{attenuation}%")

# ==================== WATER CHEMISTRY PAGE ====================
def page_water():
    st.markdown("# 💧 Water Chemistry")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Choose Starting Water Profile")
        profile = st.selectbox("Profile", list(WATER_PROFILES.keys()))
        current_water = WATER_PROFILES[profile].copy()

    with col2:
        st.markdown("### ⚙️ Adjust Minerals (ppm)")

    # Create sliders for each mineral
    col1, col2, col3 = st.columns(3)
    minerals = ['ca', 'mg', 'na', 'cl', 'so4', 'hco3']
    mineral_labels = ['Calcium', 'Magnesium', 'Sodium', 'Chloride', 'Sulfate', 'Bicarbonate']

    adjusted_water = {}
    cols = [col1, col2, col3]
    for i, (min_key, label) in enumerate(zip(minerals, mineral_labels)):
        with cols[i % 3]:
            adjusted_water[min_key] = st.slider(
                label,
                min_value=0,
                max_value=400,
                value=int(current_water[min_key]),
                step=5
            )

    # Display current vs target
    st.markdown("### 📊 Water Profile Comparison")
    comparison = pd.DataFrame({
        'Mineral': mineral_labels,
        'Starting (ppm)': [current_water[m] for m in minerals],
        'Target (ppm)': [adjusted_water[m] for m in minerals],
        'Difference': [adjusted_water[m] - current_water[m] for m in minerals]
    })
    st.dataframe(comparison, use_container_width=True)

    # Mineral additions calculator
    st.markdown("### 🧂 Mineral Additions (per gallon)")

    batch_gal = st.number_input("Batch Size (gal)", value=5, min_value=1)

    additions_needed = {}
    for salt_name, mineral_factors in MINERAL_ADDITIONS.items():
        amount_needed = 0
        for mineral, factor in mineral_factors.items():
            difference = adjusted_water[mineral] - current_water[mineral]
            if difference > 0:
                amount_needed = max(amount_needed, difference / factor)

        if amount_needed > 0:
            additions_needed[salt_name] = amount_needed

    if additions_needed:
        additions_df = pd.DataFrame({
            'Salt': list(additions_needed.keys()),
            'Per Gallon (g)': [f"{v:.2f}" for v in additions_needed.values()],
            f'Total for {batch_gal} gal (g)': [f"{v*batch_gal:.2f}" for v in additions_needed.values()]
        })
        st.dataframe(additions_df, use_container_width=True)
    else:
        st.info("✅ Target profile already matches starting water - no additions needed!")

# ==================== RECIPE BUILDER PAGE ====================
def page_builder():
    st.markdown("# 🔨 Recipe Builder")
    st.markdown("Combine ingredients to build a complete beer recipe")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Step 1️⃣: Choose Style")
        style = st.text_input("Beer Style", placeholder="e.g., IPA, Porter, Pilsner")

    with col2:
        batch_size = st.number_input("Batch Size (gal)", value=5, min_value=1)

    st.markdown("### Step 2️⃣: Select Malts")
    malts = st.multiselect("Choose malts", CLASSIC_MALTS['name'].tolist(), max_selections=10)

    malt_weights = {}
    if malts:
        cols = st.columns(len(malts))
        for i, malt in enumerate(malts):
            with cols[i]:
                malt_weights[malt] = st.number_input(
                    f"{malt} (lb)", value=2.0, min_value=0.1, step=0.5, key=f"rb_malt_{malt}"
                )

    st.markdown("### Step 3️⃣: Select Hops")
    hops_names = ['Cascade', 'Centennial', 'Chinook', 'Columbus', 'Fuggle', 'Goldings']
    hops = st.multiselect("Choose hops", hops_names, max_selections=5)

    hop_additions = {}
    if hops:
        cols = st.columns(len(hops))
        for i, hop in enumerate(hops):
            with cols[i]:
                hop_additions[hop] = st.number_input(
                    f"{hop} (oz)", value=1.0, min_value=0.1, step=0.1, key=f"rb_hop_{hop}"
                )

    st.markdown("### Step 4️⃣: Select Yeast")
    yeast = st.selectbox("Yeast", ['Ale Yeast', 'Lager Yeast', 'Saison', 'Weizen'])
    attenuation = st.slider("Attenuation %", 50, 95, 75)

    st.markdown("### Step 5️⃣: Select Water Profile")
    water_profile = st.selectbox("Water Profile", list(WATER_PROFILES.keys()))

    # Build recipe summary
    if st.button("📋 Generate Recipe", use_container_width=True):
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        st.markdown(f"## 🍺 {style} Recipe")

        col1, col2, col3, col4 = st.columns(4)

        # Calculate metrics
        srm = calculate_srm(malt_weights, batch_size) if malt_weights else 0

        total_ppg = 0
        if malt_weights:
            for malt, weight in malt_weights.items():
                malt_data = CLASSIC_MALTS[CLASSIC_MALTS['name'] == malt]
                if not malt_data.empty:
                    total_ppg += malt_data.iloc[0]['ppg'] * weight

        og = 1.0 + (total_ppg / (batch_size * 1000)) if total_ppg > 0 else 1.050
        fg = og - ((og - 1.0) * (attenuation / 100))
        abv = calculate_abv(og, fg)

        total_ibu = sum(calculate_ibu(weight, 12, 60, og) for weight in hop_additions.values()) if hop_additions else 0

        with col1:
            st.metric("OG", f"{og:.3f}")
        with col2:
            st.metric("FG", f"{fg:.3f}")
        with col3:
            st.metric("ABV", f"{abv:.2f}%")
        with col4:
            st.metric("IBU", f"{total_ibu:.0f}")

        st.markdown(f"**Color (SRM):** {srm:.1f}")
        st.markdown(f"**Yeast:** {yeast} ({attenuation}% attenuation)")
        st.markdown(f"**Water:** {water_profile}")

        st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE ROUTING ====================
page = st.session_state.page

if page == "home":
    page_home()
elif page == "malts":
    page_malts()
elif page == "combinations":
    page_combinations()
elif page == "hops":
    page_hops()
elif page == "yeasts":
    page_yeasts()
elif page == "water":
    page_water()
elif page == "builder":
    page_builder()
else:
    page_home()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
🍺 Master Brewer - Ingredients Tool
🌾 Malt | 🌿 Hops | 🧬 Yeast | 💧 Water | 🔨 Recipes
</div>
""", unsafe_allow_html=True)
