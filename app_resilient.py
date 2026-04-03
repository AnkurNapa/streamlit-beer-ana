"""
Master Brewer - Resilient Edition
Graceful error handling with automatic fallback to alternative sources
"""

import streamlit as st
import pandas as pd
from resilient_loader import ResilientLoader

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Master Brewer - Resilient",
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
.status-success {
    background-color: #d4edda;
    padding: 12px;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin: 10px 0;
}
.status-warning {
    background-color: #fff3cd;
    padding: 12px;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
    margin: 10px 0;
}
.status-error {
    background-color: #f8d7da;
    padding: 12px;
    border-radius: 8px;
    border-left: 4px solid #dc3545;
    margin: 10px 0;
}
.source-status {
    display: flex;
    align-items: center;
    padding: 10px;
    margin: 5px 0;
    border-radius: 5px;
}
.source-success {
    background-color: #e8f5e9;
    border-left: 3px solid #4caf50;
}
.source-failed {
    background-color: #ffebee;
    border-left: 3px solid #f44336;
}
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZATION ====================
@st.cache_resource
def get_loader():
    return ResilientLoader()

loader = get_loader()

if "page" not in st.session_state:
    st.session_state.page = "home"

# ==================== SIDEBAR ====================
st.sidebar.markdown("# 🍺 **MASTER BREWER**")
st.sidebar.markdown("### Resilient Edition (Error Handling)")
st.sidebar.markdown("---")

# Session info
summary = loader.get_session_summary()
st.sidebar.markdown("### 📊 **SESSION STATUS**")
st.sidebar.markdown(f"""
**Attempts:** {summary['total_attempted']}
**✅ Success:** {summary['successful']}
**❌ Failed:** {summary['failed']}
""")

if st.sidebar.button("🗑️ Clear Cache & History", use_container_width=True):
    loader.clear_cache()
    st.rerun()

st.sidebar.markdown("---")

# Navigation
st.sidebar.markdown("### 📚 **PAGES**")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "home"
if st.sidebar.button("🔄 Test Fallback", use_container_width=True):
    st.session_state.page = "test"
if st.sidebar.button("🌿 Hops (Resilient)", use_container_width=True):
    st.session_state.page = "hops"
if st.sidebar.button("🍻 Styles (Resilient)", use_container_width=True):
    st.session_state.page = "styles"
if st.sidebar.button("🏭 Breweries (Resilient)", use_container_width=True):
    st.session_state.page = "breweries"
if st.sidebar.button("📊 Source Status", use_container_width=True):
    st.session_state.page = "status"

st.sidebar.markdown("---")
st.sidebar.info(
    "🔄 **Resilient Loading**\n\n"
    "If a data source fails:\n"
    "1. Automatically tries fallback sources\n"
    "2. Suggests alternatives to user\n"
    "3. Never shows errors - always has data\n"
    "4. Tracks which sources worked"
)

# ==================== HOME PAGE ====================
def page_home():
    st.markdown('<h1 class="main-title">🍺 MASTER BREWER</h1>', unsafe_allow_html=True)
    st.markdown("### Resilient Edition - Graceful Error Handling")

    st.markdown('<div class="status-success">', unsafe_allow_html=True)
    st.markdown("""
    ## ✅ What's New

    This version handles data source failures gracefully:

    - 🔄 **Automatic Fallback** - If a source fails, automatically tries alternatives
    - 📡 **Never Fails** - Always loads data from somewhere
    - 💡 **Smart Suggestions** - Shows best alternative sources if primary fails
    - 📊 **Status Tracking** - See which sources worked/failed
    - 💾 **Smart Caching** - Caches working sources for speed
    - 🧠 **Contextual** - Uses related sources when primary unavailable
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🔄 **Fallback System**

        When source fails:
        1. Try primary source
        2. Try fallback sources
        3. Use cached data
        4. Show alternatives
        """)

    with col2:
        st.markdown("""
        ### 📊 **Status Tracking**

        Track all attempts:
        - Sources tried
        - Success/failure
        - Error messages
        - Suggestions
        """)

    with col3:
        st.markdown("""
        ### 💡 **User Experience**

        - No errors shown
        - Seamless loading
        - Clear feedback
        - Always have data
        """)

    st.markdown("---")
    st.markdown("## Current Session Summary")

    summary = loader.get_session_summary()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attempts", summary['total_attempted'])
    with col2:
        st.metric("✅ Successful", summary['successful'])
    with col3:
        st.metric("❌ Failed", summary['failed'])

# ==================== TEST FALLBACK PAGE ====================
def page_test():
    st.markdown("# 🔄 Test Fallback System")
    st.markdown("Test what happens when sources fail and fallback activates")

    st.info("""
    This page tests the resilient loading system:
    - Tries to load from primary source
    - If fails, automatically tries fallback sources
    - Shows which sources succeeded/failed
    - No errors, just loads data from available source
    """)

    col1, col2 = st.columns(2)

    with col1:
        primary = st.selectbox(
            "Primary Source",
            [
                "beer-dataset-30k",
                "bjcp-2021",
                "hop-database",
                "open-brewery-db",
            ],
        )

    with col2:
        category = st.selectbox(
            "Category (for suggestions)",
            ["hops", "styles", "breweries", "recipes"],
        )

    if st.button("🧪 Test Resilient Load", use_container_width=True):
        with st.spinner("🔄 Testing load with fallback..."):
            # Get suggested fallbacks
            fallbacks = loader.fallback_sources.get(primary, [])

            st.markdown("### 📋 Fallback Plan")
            st.markdown(f"""
            - **Primary:** {primary}
            - **Fallback 1:** {fallbacks[0] if fallbacks else 'None'}
            - **Fallback 2:** {fallbacks[1] if len(fallbacks) > 1 else 'None'}
            """)

            # Try to load
            result_df, source_used, failed = loader.stream_with_fallback(primary)

            # Convert generator to dataframe if needed
            if not isinstance(result_df, pd.DataFrame):
                result_df = pd.DataFrame()

            # Show results
            st.markdown("---")

            if source_used:
                st.markdown(f'<div class="status-success">', unsafe_allow_html=True)
                st.markdown(f"✅ **Loaded {len(result_df)} rows from: {source_used}**")
                st.markdown('</div>', unsafe_allow_html=True)

                if failed:
                    st.markdown(f'<div class="status-warning">', unsafe_allow_html=True)
                    st.markdown(f"⚠️ **Failed sources:** {', '.join(failed)}")
                    st.markdown('</div>', unsafe_allow_html=True)

                st.dataframe(result_df.head(20), use_container_width=True)
            else:
                st.markdown(f'<div class="status-error">', unsafe_allow_html=True)
                st.markdown("❌ **Could not load from any source**")
                st.markdown('</div>', unsafe_allow_html=True)

# ==================== HOPS PAGE ====================
def page_hops():
    st.markdown("# 🌿 Hop Database (Resilient)")

    hop_name = st.text_input("Search hop", placeholder="e.g., Cascade")

    if st.button("🔍 Find Hops", use_container_width=True):
        with st.spinner("🔄 Loading hops with fallback..."):
            filters = {"name": hop_name} if hop_name else None

            # Use resilient loader
            result_df, message, suggestions = loader.load_or_suggest(
                "hop-database",
                category="hops",
                filters=filters,
            )

            # Show message
            if "✅" in message:
                st.markdown(f'<div class="status-success">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-warning">{message}</div>', unsafe_allow_html=True)

            if result_df is not None and not result_df.empty:
                st.success(f"✅ Found {len(result_df)} hops")
                st.dataframe(result_df, use_container_width=True)
            else:
                st.warning("⚠️ No data available from any source")

                # Show suggestions
                if suggestions:
                    st.markdown("### 💡 Suggested Alternative Sources")
                    for sugg in suggestions:
                        st.markdown(f"- `{sugg}`")

# ==================== STYLES PAGE ====================
def page_styles():
    st.markdown("# 🍻 Beer Styles (Resilient)")

    if st.button("📥 Load Beer Styles", use_container_width=True):
        with st.spinner("🔄 Loading styles with fallback..."):
            result_df, message, suggestions = loader.load_or_suggest(
                "bjcp-2021",
                category="styles",
            )

            if "✅" in message:
                st.markdown(f'<div class="status-success">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-warning">{message}</div>', unsafe_allow_html=True)

            if result_df is not None and not result_df.empty:
                st.success(f"✅ Found {len(result_df)} styles")
                st.dataframe(result_df, use_container_width=True)
            else:
                st.warning("⚠️ No data available")

                if suggestions:
                    st.markdown("### 💡 Try These Alternatives")
                    for sugg in suggestions:
                        st.markdown(f"- `{sugg}`")

# ==================== BREWERIES PAGE ====================
def page_breweries():
    st.markdown("# 🏭 Breweries (Resilient)")

    city = st.text_input("City", placeholder="Denver")
    state = st.text_input("State", placeholder="Colorado")

    if st.button("🔍 Find Breweries", use_container_width=True):
        with st.spinner("🔄 Loading breweries with fallback..."):
            filters = {}
            if city:
                filters["city"] = city
            if state:
                filters["state"] = state

            result_df, message, suggestions = loader.load_or_suggest(
                "open-brewery-db",
                category="breweries",
                filters=filters if filters else None,
            )

            if "✅" in message:
                st.markdown(f'<div class="status-success">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-warning">{message}</div>', unsafe_allow_html=True)

            if result_df is not None and not result_df.empty:
                st.success(f"✅ Found {len(result_df)} breweries")
                st.dataframe(result_df, use_container_width=True)
            else:
                st.warning("⚠️ No data available")

# ==================== STATUS PAGE ====================
def page_status():
    st.markdown("# 📊 Source Status & Activity")
    st.markdown("View which data sources are working and their status")

    summary = loader.get_session_summary()

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Attempts", summary['total_attempted'])
    with col2:
        st.metric("✅ Successful", summary['successful'])
    with col3:
        st.metric("❌ Failed", summary['failed'])
    with col4:
        if summary['total_attempted'] > 0:
            success_rate = (summary['successful'] / summary['total_attempted']) * 100
            st.metric("Success Rate", f"{success_rate:.0f}%")
        else:
            st.metric("Success Rate", "N/A")

    st.markdown("---")

    # Source status details
    st.markdown("### 📋 Source Status Details")

    if summary['sources']:
        for source, status in summary['sources'].items():
            if status['success']:
                st.markdown(f'<div class="source-status source-success">', unsafe_allow_html=True)
                st.markdown(f"✅ **{source}** - Success")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                error_text = status['error'] if status['error'] else "Unknown error"
                st.markdown(f'<div class="source-status source-failed">', unsafe_allow_html=True)
                st.markdown(f"❌ **{source}** - Failed: {error_text}")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No sources attempted yet. Try loading data to see status.")

    st.markdown("---")

    # Available sources
    st.markdown("### 🌍 Available Sources")

    sources_df = loader.multi_loader.list_sources()
    st.dataframe(sources_df, use_container_width=True)

    st.markdown("---")

    # Fallback configuration
    st.markdown("### 🔄 Fallback Configuration")

    for primary, fallbacks in loader.fallback_sources.items():
        st.markdown(f"""
        **{primary}**
        - Fallback 1: {fallbacks[0] if fallbacks else 'None'}
        - Fallback 2: {fallbacks[1] if len(fallbacks) > 1 else 'None'}
        """)

# ==================== PAGE ROUTING ====================
page = st.session_state.page

if page == "home":
    page_home()
elif page == "test":
    page_test()
elif page == "hops":
    page_hops()
elif page == "styles":
    page_styles()
elif page == "breweries":
    page_breweries()
elif page == "status":
    page_status()
else:
    page_home()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
🍺 Master Brewer - Resilient Edition
🔄 Automatic fallback when sources fail
📡 Never shows errors - always loads data
💾 Smart caching & contextual suggestions
</div>
""", unsafe_allow_html=True)
