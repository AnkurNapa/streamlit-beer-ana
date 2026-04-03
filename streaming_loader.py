"""
Streaming Data Loader - Load data live from sources
Session-based caching with automatic cleanup
No permanent storage needed
"""

import streamlit as st
import pandas as pd
from typing import Optional, Generator, Dict, List
import gc
from functools import lru_cache
import json
from firecrawl import FirecrawlApp
import os


class StreamingDataLoader:
    """Load and stream data live from Beer Analytics with session-based caching"""

    def __init__(self):
        """Initialize streaming loader with session cache"""
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        self.app = FirecrawlApp(api_key=self.api_key) if self.api_key else None

        # Session-based cache (cleared when session ends)
        if "cache" not in st.session_state:
            st.session_state.cache = {}
        if "cache_timestamps" not in st.session_state:
            st.session_state.cache_timestamps = {}

    def _get_cache_key(self, endpoint: str, params: dict = None) -> str:
        """Generate cache key for endpoint"""
        param_str = json.dumps(params, sort_keys=True) if params else ""
        return f"{endpoint}:{param_str}"

    def _is_cache_valid(self, key: str, max_age: int = 300) -> bool:
        """Check if cache is still valid (5 min default)"""
        import time
        if key not in st.session_state.cache_timestamps:
            return False
        return time.time() - st.session_state.cache_timestamps[key] < max_age

    def _cache_data(self, key: str, data):
        """Store data in session cache"""
        import time
        st.session_state.cache[key] = data
        st.session_state.cache_timestamps[key] = time.time()

    def _get_cached(self, key: str):
        """Get data from cache if valid"""
        if key in st.session_state.cache and self._is_cache_valid(key):
            return st.session_state.cache[key]
        return None

    def clear_session_cache(self):
        """Clear all session cache"""
        st.session_state.cache.clear()
        st.session_state.cache_timestamps.clear()
        gc.collect()

    # ==================== STREAMING HOPS ====================

    def stream_hops(
        self,
        alpha_acids_min: Optional[float] = None,
        alpha_acids_max: Optional[float] = None,
        origin: Optional[str] = None,
        page_size: int = 50,
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream hops data in chunks"""
        cache_key = self._get_cache_key("hops", {
            "alpha_acids_min": alpha_acids_min,
            "alpha_acids_max": alpha_acids_max,
            "origin": origin,
        })

        # Check cache first
        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            result = self.app.scrape_url(
                "https://www.beer-analytics.com/hops",
                {
                    "extractionSchema": {
                        "type": "object",
                        "properties": {
                            "hops": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "alpha_acids": {"type": "number"},
                                        "origin": {"type": "string"},
                                        "purpose": {"type": "string"},
                                        "flavor": {"type": "array"},
                                        "recipes": {"type": "number"},
                                    },
                                },
                            }
                        },
                    }
                },
            )

            hops_list = result.get("data", {}).get("hops", [])
            df = pd.DataFrame(hops_list)

            # Apply filters
            if alpha_acids_min is not None:
                df = df[df["alpha_acids"] >= alpha_acids_min]
            if alpha_acids_max is not None:
                df = df[df["alpha_acids"] <= alpha_acids_max]
            if origin:
                df = df[df["origin"].str.lower().str.contains(origin.lower(), na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()  # Free memory

            # Cache final result
            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error streaming hops: {e}")
            return

    # ==================== STREAMING YEASTS ====================

    def stream_yeasts(
        self, yeast_type: Optional[str] = None, page_size: int = 50
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream yeasts data in chunks"""
        cache_key = self._get_cache_key("yeasts", {"yeast_type": yeast_type})

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            result = self.app.scrape_url(
                "https://www.beer-analytics.com/yeasts",
                {
                    "extractionSchema": {
                        "type": "object",
                        "properties": {
                            "yeasts": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string"},
                                        "temperature_min": {"type": "number"},
                                        "temperature_max": {"type": "number"},
                                        "attenuation": {"type": "number"},
                                        "recipes": {"type": "number"},
                                    },
                                },
                            }
                        },
                    }
                },
            )

            yeasts_list = result.get("data", {}).get("yeasts", [])
            df = pd.DataFrame(yeasts_list)

            # Apply filters
            if yeast_type:
                df = df[df["type"].str.lower().str.contains(yeast_type.lower(), na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error streaming yeasts: {e}")
            return

    # ==================== STREAMING RECIPES ====================

    def stream_recipes(
        self,
        style: Optional[str] = None,
        ibu_min: Optional[int] = None,
        ibu_max: Optional[int] = None,
        abv_min: Optional[float] = None,
        abv_max: Optional[float] = None,
        page_size: int = 100,
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream recipes data in chunks (lazy load)"""
        cache_key = self._get_cache_key("recipes", {
            "style": style,
            "ibu_min": ibu_min,
            "ibu_max": ibu_max,
            "abv_min": abv_min,
            "abv_max": abv_max,
        })

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            # Fetch recipes in pages
            result = self.app.scrape_url(
                "https://www.beer-analytics.com/recipes",
                {
                    "extractionSchema": {
                        "type": "object",
                        "properties": {
                            "recipes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "style": {"type": "string"},
                                        "ibu": {"type": "number"},
                                        "abv": {"type": "number"},
                                        "color": {"type": "number"},
                                        "rating": {"type": "number"},
                                    },
                                },
                            }
                        },
                    }
                },
            )

            recipes_list = result.get("data", {}).get("recipes", [])
            df = pd.DataFrame(recipes_list)

            # Apply filters
            if style:
                df = df[df["style"].str.lower().str.contains(style.lower(), na=False)]
            if ibu_min is not None:
                df = df[df["ibu"] >= ibu_min]
            if ibu_max is not None:
                df = df[df["ibu"] <= ibu_max]
            if abv_min is not None:
                df = df[df["abv"] >= abv_min]
            if abv_max is not None:
                df = df[df["abv"] <= abv_max]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error streaming recipes: {e}")
            return

    # ==================== STREAMING FERMENTABLES ====================

    def stream_fermentables(
        self, grain_type: Optional[str] = None, page_size: int = 50
    ) -> Generator[pd.DataFrame, None, None]:
        """Stream fermentables in chunks"""
        cache_key = self._get_cache_key("fermentables", {"grain_type": grain_type})

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            result = self.app.scrape_url(
                "https://www.beer-analytics.com/fermentables",
                {
                    "extractionSchema": {
                        "type": "object",
                        "properties": {
                            "fermentables": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string"},
                                        "color": {"type": "number"},
                                        "ppg": {"type": "number"},
                                        "recipes": {"type": "number"},
                                    },
                                },
                            }
                        },
                    }
                },
            )

            fermentables_list = result.get("data", {}).get("fermentables", [])
            df = pd.DataFrame(fermentables_list)

            # Apply filters
            if grain_type:
                df = df[df["type"].str.lower().str.contains(grain_type.lower(), na=False)]

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error streaming fermentables: {e}")
            return

    # ==================== STREAMING BEER STYLES ====================

    def stream_beer_styles(self, page_size: int = 50) -> Generator[pd.DataFrame, None, None]:
        """Stream beer styles in chunks"""
        cache_key = self._get_cache_key("beer_styles")

        cached = self._get_cached(cache_key)
        if cached is not None:
            yield cached
            return

        try:
            result = self.app.scrape_url(
                "https://www.beer-analytics.com/beer-styles",
                {
                    "extractionSchema": {
                        "type": "object",
                        "properties": {
                            "styles": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "category": {"type": "string"},
                                        "ibu_min": {"type": "number"},
                                        "ibu_max": {"type": "number"},
                                        "abv_min": {"type": "number"},
                                        "abv_max": {"type": "number"},
                                        "color_min": {"type": "number"},
                                        "color_max": {"type": "number"},
                                    },
                                },
                            }
                        },
                    }
                },
            )

            styles_list = result.get("data", {}).get("styles", [])
            df = pd.DataFrame(styles_list)

            # Stream in chunks
            for i in range(0, len(df), page_size):
                chunk = df.iloc[i : i + page_size]
                yield chunk
                gc.collect()

            self._cache_data(cache_key, df)

        except Exception as e:
            st.error(f"Error streaming beer styles: {e}")
            return

    # ==================== UTILITY METHODS ====================

    def get_session_memory_usage(self) -> Dict[str, str]:
        """Get current session memory usage"""
        import sys

        cache_size = sum(
            sys.getsizeof(v) for v in st.session_state.cache.values()
        ) / (1024 * 1024)

        return {
            "cached_items": len(st.session_state.cache),
            "cache_size_mb": f"{cache_size:.2f} MB",
            "items": list(st.session_state.cache.keys()),
        }

    def stream_search_with_progress(
        self,
        data_type: str,
        filters: Dict,
        progress_bar=None,
    ) -> pd.DataFrame:
        """Stream data and show progress"""
        all_chunks = []

        if data_type == "recipes":
            generator = self.stream_recipes(**filters)
        elif data_type == "hops":
            generator = self.stream_hops(**filters)
        elif data_type == "yeasts":
            generator = self.stream_yeasts(**filters)
        elif data_type == "fermentables":
            generator = self.stream_fermentables(**filters)
        elif data_type == "beer_styles":
            generator = self.stream_beer_styles()
        else:
            return pd.DataFrame()

        for chunk in generator:
            all_chunks.append(chunk)
            if progress_bar:
                progress_bar.progress(min(len(all_chunks) * 10, 90))

        if all_chunks:
            result = pd.concat(all_chunks, ignore_index=True)
            if progress_bar:
                progress_bar.progress(100)
            return result

        return pd.DataFrame()

    def prefetch_top_items(self, data_type: str, limit: int = 10) -> pd.DataFrame:
        """Prefetch only top items (popular/trending)"""
        cache_key = self._get_cache_key(f"top_{data_type}", {"limit": limit})

        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        try:
            if data_type == "hops":
                # Get only top hops by recipe count
                for chunk in self.stream_hops():
                    result = chunk.nlargest(limit, "recipes") if "recipes" in chunk.columns else chunk.head(limit)
                    self._cache_data(cache_key, result)
                    return result

            elif data_type == "yeasts":
                for chunk in self.stream_yeasts():
                    result = chunk.nlargest(limit, "recipes") if "recipes" in chunk.columns else chunk.head(limit)
                    self._cache_data(cache_key, result)
                    return result

            elif data_type == "fermentables":
                for chunk in self.stream_fermentables():
                    result = chunk.nlargest(limit, "recipes") if "recipes" in chunk.columns else chunk.head(limit)
                    self._cache_data(cache_key, result)
                    return result

        except Exception as e:
            st.error(f"Error prefetching {data_type}: {e}")

        return pd.DataFrame()
