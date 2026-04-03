"""
Resilient Multi-Source Loader with Fallback
Handles data source failures gracefully with automatic fallback
"""

import streamlit as st
import pandas as pd
import json
import logging
from typing import Optional, Generator, Dict, List, Tuple
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import gc
from multi_source_loader import MultiSourceLoader

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResilientLoader:
    """Load data with automatic fallback when sources fail"""

    def __init__(self):
        """Initialize resilient loader with fallback sources"""
        self.multi_loader = MultiSourceLoader()

        # Session-based tracking
        if "resilient_cache" not in st.session_state:
            st.session_state.resilient_cache = {}
        if "resilient_timestamps" not in st.session_state:
            st.session_state.resilient_timestamps = {}
        if "source_status" not in st.session_state:
            st.session_state.source_status = {}  # Track which sources worked/failed

        # Fallback mappings: when source fails, try these next
        self.fallback_sources = {
            "beer-dataset-30k": [
                "open-brewery-db",
                "common-beer-data",
            ],
            "bjcp-2021": [
                "common-beer-data",
            ],
            "hop-database": [
                "common-beer-data",
            ],
            "open-brewery-db": [
                "beer-dataset-30k",
                "common-beer-data",
            ],
            "common-beer-data": [
                "beer-dataset-30k",
                "open-brewery-db",
            ],
        }

        # Related sources for contextual suggestions
        self.related_sources = {
            "hops": ["common-beer-data", "beer-dataset-30k"],
            "styles": ["bjcp-2021", "common-beer-data"],
            "breweries": ["open-brewery-db", "beer-dataset-30k"],
            "recipes": ["beer-dataset-30k", "common-beer-data"],
        }

    def _get_cache_key(self, source: str, params: dict = None) -> str:
        """Generate cache key"""
        param_str = json.dumps(params, sort_keys=True) if params else ""
        return f"{source}:{param_str}"

    def _is_cache_valid(self, key: str, max_age: int = 300) -> bool:
        """Check if cache is valid (5 min default)"""
        import time
        if key not in st.session_state.resilient_timestamps:
            return False
        return time.time() - st.session_state.resilient_timestamps[key] < max_age

    def _cache_data(self, key: str, data, source: str):
        """Store data in session cache with source info"""
        import time
        st.session_state.resilient_cache[key] = {
            "data": data,
            "source": source,
            "timestamp": time.time(),
        }
        st.session_state.resilient_timestamps[key] = time.time()

    def _get_cached(self, key: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Get data from cache if valid. Returns (data, source_used)"""
        if key in st.session_state.resilient_cache and self._is_cache_valid(key):
            cached = st.session_state.resilient_cache[key]
            return cached["data"], cached["source"]
        return None, None

    def _record_source_status(self, source: str, success: bool, error: str = None):
        """Record which sources worked/failed"""
        if "sources" not in st.session_state.source_status:
            st.session_state.source_status["sources"] = {}

        st.session_state.source_status["sources"][source] = {
            "success": success,
            "error": error,
        }

    def get_source_status(self) -> Dict:
        """Get status of all data sources attempted"""
        return st.session_state.source_status.get("sources", {})

    def stream_with_fallback(
        self,
        primary_source: str,
        filters: Optional[Dict] = None,
        page_size: int = 100,
        timeout: int = 5,
    ) -> Tuple[Generator[pd.DataFrame, None, None], str, List[str]]:
        """
        Stream data with automatic fallback

        Returns:
            (generator, source_used, failed_sources)
        """
        cache_key = self._get_cache_key(primary_source, filters)

        # Check cache first
        cached_data, cached_source = self._get_cached(cache_key)
        if cached_data is not None:
            logger.info(f"Cache hit: {primary_source} (from {cached_source})")
            yield cached_data
            return cached_data, cached_source, []

        # Try sources in order: primary + fallbacks
        sources_to_try = [primary_source]
        if primary_source in self.fallback_sources:
            sources_to_try.extend(self.fallback_sources[primary_source])

        failed_sources = []

        for source in sources_to_try:
            try:
                logger.info(f"Attempting to load from: {source}")

                if source not in self.multi_loader.sources:
                    logger.warning(f"Source {source} not found, skipping")
                    failed_sources.append(source)
                    continue

                source_type = self.multi_loader.sources[source]["type"]

                # Try to load based on source type
                if source_type == "json":
                    generator = self.multi_loader.stream_json_source(source, filters, page_size)
                elif source_type == "csv":
                    generator = self.multi_loader.stream_csv_source(source, filters, page_size)
                else:
                    logger.warning(f"Unknown source type: {source_type}")
                    failed_sources.append(source)
                    continue

                # Consume generator and collect data
                all_data = []
                for chunk in generator:
                    all_data.append(chunk)

                if all_data:
                    result_df = pd.concat(all_data, ignore_index=True)
                    # Cache the successful result
                    self._cache_data(cache_key, result_df, source)
                    self._record_source_status(source, True)

                    logger.info(f"✅ Successfully loaded {len(result_df)} rows from {source}")
                    yield result_df
                    return result_df, source, failed_sources

            except (URLError, HTTPError, Exception) as e:
                error_msg = str(e)
                logger.warning(f"❌ Failed to load from {source}: {error_msg}")
                self._record_source_status(source, False, error_msg)
                failed_sources.append(source)
                continue

        # All sources failed
        logger.error(f"All sources failed for {primary_source}")
        self._record_source_status(primary_source, False, "All fallback sources failed")
        yield pd.DataFrame()
        return pd.DataFrame(), None, failed_sources

    def stream_multiple_sources(
        self,
        sources: List[str],
        filters: Optional[Dict] = None,
        combine: bool = True,
    ) -> Tuple[pd.DataFrame, Dict[str, bool]]:
        """
        Try to load from multiple sources, return success/failure status

        Returns:
            (combined_dataframe, status_dict)
        """
        results = {}
        all_data = []

        for source in sources:
            try:
                logger.info(f"Loading: {source}")

                if source not in self.multi_loader.sources:
                    results[source] = {"success": False, "rows": 0, "error": "Source not found"}
                    continue

                source_type = self.multi_loader.sources[source]["type"]

                if source_type == "json":
                    generator = self.multi_loader.stream_json_source(source, filters)
                elif source_type == "csv":
                    generator = self.multi_loader.stream_csv_source(source, filters)
                else:
                    results[source] = {"success": False, "rows": 0, "error": f"Unknown type: {source_type}"}
                    continue

                # Collect data
                df_list = [chunk for chunk in generator]
                if df_list:
                    df = pd.concat(df_list, ignore_index=True)
                    results[source] = {"success": True, "rows": len(df), "error": None}
                    all_data.append(df)
                    logger.info(f"✅ {source}: {len(df)} rows")
                else:
                    results[source] = {"success": False, "rows": 0, "error": "No data returned"}

            except Exception as e:
                error_msg = str(e)
                results[source] = {"success": False, "rows": 0, "error": error_msg}
                logger.error(f"❌ {source}: {error_msg}")

        # Combine results
        if combine and all_data:
            combined = pd.concat(all_data, ignore_index=True)
            return combined, results

        if all_data:
            return all_data[0] if len(all_data) == 1 else pd.concat(all_data, ignore_index=True), results

        return pd.DataFrame(), results

    def get_suggested_sources(self, category: str) -> List[str]:
        """Get suggested sources for a category"""
        return self.related_sources.get(category, [])

    def load_or_suggest(
        self,
        primary_source: str,
        category: str = None,
        filters: Optional[Dict] = None,
    ) -> Tuple[Optional[pd.DataFrame], str, List[str]]:
        """
        Load from primary source with smart suggestions if it fails

        Returns:
            (dataframe, message, suggestions)
        """
        try:
            for result_df in self.stream_with_fallback(primary_source, filters):
                if not result_df.empty:
                    return result_df, f"✅ Loaded from primary source", []

        except Exception as e:
            logger.error(f"Error loading {primary_source}: {e}")

        # If we get here, primary source failed
        logger.info(f"Primary source {primary_source} failed, getting suggestions")

        suggestions = self.get_suggested_sources(category or primary_source)

        message = (
            f"⚠️ Could not load from {primary_source}.\n\n"
            f"**Suggested alternatives:**\n"
        )
        for sugg in suggestions:
            message += f"- {sugg}\n"

        return None, message, suggestions

    def get_session_summary(self) -> Dict:
        """Get summary of session activity"""
        status = self.get_source_status()
        successful = sum(1 for s in status.values() if s.get("success", False))
        failed = len(status) - successful

        return {
            "total_attempted": len(status),
            "successful": successful,
            "failed": failed,
            "sources": status,
        }

    def clear_cache(self):
        """Clear all cached data"""
        st.session_state.resilient_cache.clear()
        st.session_state.resilient_timestamps.clear()
        st.session_state.source_status.clear()
        gc.collect()
