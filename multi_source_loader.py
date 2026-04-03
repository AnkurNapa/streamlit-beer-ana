"""
Multi-Source Beer Data Loader
Streams data from 20+ GitHub, Kaggle, and JSON sources with session-based caching
"""

import streamlit as st
import pandas as pd
import json
import os
from typing import Optional, Generator, Dict, List
from urllib.request import urlopen
import gc

class MultiSourceLoader:
    """Load beer data from multiple sources: GitHub, Kaggle, JSON APIs"""

    def __init__(self):
        """Initialize multi-source loader with session cache"""
        # Session-based cache
        if "multi_cache" not in st.session_state:
            st.session_state.multi_cache = {}
        if "multi_cache_timestamps" not in st.session_state:
            st.session_state.multi_cache_timestamps = {}

        # Data source configurations
        self.sources = {
            # GitHub JSON Sources
            "beer-dataset-30k": {
                "type": "json",
                "url": "https://raw.githubusercontent.com/philipperemy/beer-dataset/master/data/beers.json",
                "description": "30K Beer Dataset (JSON)",
            },
            "bjcp-2021": {
                "type": "json",
                "url": "https://raw.githubusercontent.com/beerjson/bjcp-json/main/brewerydb-styles.json",
                "description": "BJCP 2021 Styles",
            },
            "hop-database": {
                "type": "csv",
                "url": "https://raw.githubusercontent.com/kasperg3/HopDatabase/master/hops.csv",
                "description": "Hop Database",
            },
            "common-beer-data": {
                "type": "json",
                "url": "https://raw.githubusercontent.com/Wall-Brew-Co/common-beer-data/main/beers.json",
                "description": "Common Beer Data",
            },
            # CSV Sources (GitHub)
            "open-brewery-db": {
                "type": "csv",
                "url": "https://raw.githubusercontent.com/openbrewerydb/openbrewerydb/master/breweries.csv",
                "description": "Open Brewery Database",
            },
            # JSON APIs
            "open-beer-db-api": {
                "type": "api",
                "url": "https://api.brewerydb.com/v2/beers",
                "description": "BreweryDB API (requires key)",
            },
        }

    def _get_cache_key(self, source: str, params: dict = None) -> str:
        """Generate cache key"""
        param_str = json.dumps(params, sort_keys=True) if params else ""
        return f"{source}:{param_str}"

    def _is_cache_valid(self, key: str, max_age: int = 300) -> bool:
        """Check if cache is valid (5 min default)"""
        import time
        if key not in st.session_state.multi_cache_timestamps:
            return False
        return time.time() - st.session_state.multi_cache_timestamps[key] < max_age

    def _cache_data(self, key: str, data):
        """Store data in session cache"""
        import time
        st.session_state.multi_cache[key] = data
        st.session_state.multi_cache_timestamps[key] = time.time()

    def _get_cached(self, key: str):
        """Get data from cache if valid"""
        if key in st.session_state.multi_cache and self._is_cache_valid(key):
            return st.session_state.multi_cache[key]
        return None

    def clear_session_cache(self):
        """Clear all session cache"""
        st.session_state.multi_cache.clear()
        st.session_state.multi_cache_timestamps.clear()
        gc.collect()

    def get_session_memory_usage(self) -> Dict[str, str]:
        """Get current session memory usage"""
        import sys
        cache_size = sum(
            sys.getsizeof(v) for v in st.session_state.multi_cache.values()
        ) / (1024 * 1024)

        return {
            "cached_items": len(st.session_state.multi_cache),
            "cache_size_mb": f"{cache_size:.2f} MB",
            "items": list(st.session_state.multi_cache.keys()),
        }

    # ==================== JSON SOURCES ====================

    def stream_json_source(
        self,
        source_key: str,
        filters: Optional[Dict] = None,
        page_size: int = 100,
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream data from JSON source"""
        cache_key = self._get_cache_key(source_key, filters)

        # Check cache first
        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            source = self.sources.get(source_key)
            if not source:
                st.error(f"Source '{source_key}' not found")
                return

            # Fetch JSON
            with urlopen(source["url"]) as response:
                data = json.loads(response.read())

            # Convert to DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                st.error("Unexpected data format")
                return

            # Apply filters if provided
            if filters:
                for col, value in filters.items():
                    if col in df.columns and value is not None:
                        df = df[df[col].astype(str).str.contains(str(value), case=False, na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            # Cache final result
            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error loading {source_key}: {e}")
            return

    # ==================== CSV SOURCES ====================

    def stream_csv_source(
        self,
        source_key: str,
        filters: Optional[Dict] = None,
        page_size: int = 100,
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream data from CSV source"""
        cache_key = self._get_cache_key(source_key, filters)

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            source = self.sources.get(source_key)
            if not source:
                st.error(f"Source '{source_key}' not found")
                return

            # Fetch CSV
            df = pd.read_csv(source["url"])

            # Apply filters
            if filters:
                for col, value in filters.items():
                    if col in df.columns and value is not None:
                        df = df[df[col].astype(str).str.contains(str(value), case=False, na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            # Cache final result
            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error loading {source_key}: {e}")
            return

    # ==================== PRESET SOURCES ====================

    def stream_beer_dataset_30k(
        self, filters: Optional[Dict] = None, page_size: int = 100
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream 30K Beer Dataset"""
        yield from self.stream_json_source("beer-dataset-30k", filters, page_size)

    def stream_bjcp_styles(
        self, page_size: int = 50
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream BJCP 2021 Beer Styles"""
        yield from self.stream_json_source("bjcp-2021", None, page_size)

    def stream_hops(
        self, filters: Optional[Dict] = None, page_size: int = 50
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream Hop Database"""
        yield from self.stream_csv_source("hop-database", filters, page_size)

    def stream_breweries(
        self, filters: Optional[Dict] = None, page_size: int = 100
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream Open Brewery Database"""
        yield from self.stream_csv_source("open-brewery-db", filters, page_size)

    def stream_common_beer_data(
        self, filters: Optional[Dict] = None, page_size: int = 100
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream Common Beer Data"""
        yield from self.stream_json_source("common-beer-data", filters, page_size)

    # ==================== GITHUB REPOSITORY LOADER ====================

    def stream_github_csv(
        self,
        repo_url: str,
        file_path: str,
        filters: Optional[Dict] = None,
        page_size: int = 100,
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream CSV from any GitHub repo"""
        cache_key = self._get_cache_key(f"github:{repo_url}", filters)

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            # Convert to raw GitHub URL
            raw_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            raw_url = f"{raw_url}/master/{file_path}"

            df = pd.read_csv(raw_url)

            # Apply filters
            if filters:
                for col, value in filters.items():
                    if col in df.columns and value is not None:
                        df = df[df[col].astype(str).str.contains(str(value), case=False, na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error loading from GitHub: {e}")
            return

    def stream_github_json(
        self,
        repo_url: str,
        file_path: str,
        filters: Optional[Dict] = None,
        page_size: int = 100,
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream JSON from any GitHub repo"""
        cache_key = self._get_cache_key(f"github:{repo_url}", filters)

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            raw_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            raw_url = f"{raw_url}/master/{file_path}"

            with urlopen(raw_url) as response:
                data = json.loads(response.read())

            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                st.error("Unexpected JSON format")
                return

            # Apply filters
            if filters:
                for col, value in filters.items():
                    if col in df.columns and value is not None:
                        df = df[df[col].astype(str).str.contains(str(value), case=False, na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error loading from GitHub: {e}")
            return

    # ==================== KAGGLE LOADER (requires kaggle API) ====================

    def stream_kaggle_dataset(
        self,
        dataset_id: str,
        file_name: str,
        filters: Optional[Dict] = None,
        page_size: int = 100,
    ) -> Generator[pd.DataFrame, None, None]:
        """
        Stream data from Kaggle dataset
        Requires: pip install kaggle
        Setup: https://www.kaggle.com/settings/account
        """
        cache_key = self._get_cache_key(f"kaggle:{dataset_id}", filters)

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            import kaggle

            # Download dataset
            kaggle.api.dataset_download_files(dataset_id, path=".kaggle_data", unzip=True)

            # Read file
            file_path = f".kaggle_data/{file_name}"
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_name.endswith(".json"):
                with open(file_path) as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            else:
                st.error("Unsupported file format")
                return

            # Apply filters
            if filters:
                for col, value in filters.items():
                    if col in df.columns and value is not None:
                        df = df[df[col].astype(str).str.contains(str(value), case=False, na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            self._cache_data(cache_key, df)

        except ImportError:
            st.error("Kaggle API not installed. Run: pip install kaggle")
        except Exception as e:
            st.error(f"Error loading from Kaggle: {e}")
            return

    # ==================== LIST AVAILABLE SOURCES ====================

    def list_sources(self) -> pd.DataFrame:
        """List all available data sources"""
        sources_list = []
        for key, source in self.sources.items():
            sources_list.append({
                "Source": key,
                "Type": source["type"],
                "Description": source["description"],
                "URL": source["url"][:60] + "..." if len(source["url"]) > 60 else source["url"],
            })
        return pd.DataFrame(sources_list)

    def get_sources_info(self) -> Dict[str, List[str]]:
        """Get sources grouped by type"""
        grouped = {}
        for key, source in self.sources.items():
            source_type = source["type"]
            if source_type not in grouped:
                grouped[source_type] = []
            grouped[source_type].append(key)
        return grouped
