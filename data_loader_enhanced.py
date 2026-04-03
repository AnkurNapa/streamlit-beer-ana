"""
Enhanced data loader for complete Beer Analytics data
Provides advanced filtering, search, and analytics
"""

import json
from pathlib import Path
from typing import Optional
import pandas as pd


class EnhancedDataLoader:
    """Load and manage all Beer Analytics data with advanced features"""

    def __init__(self, data_dir: str = "data/beer-analytics-full"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_hops(self) -> Optional[pd.DataFrame]:
        """Load detailed hops data"""
        filepath = self.data_dir / "hops_detailed.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            hops_list = data.get("hops", [])
            if hops_list:
                return pd.DataFrame(hops_list)
        return None

    def load_yeasts(self) -> Optional[pd.DataFrame]:
        """Load detailed yeasts data"""
        filepath = self.data_dir / "yeasts_detailed.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            yeasts_list = data.get("yeasts", [])
            if yeasts_list:
                return pd.DataFrame(yeasts_list)
        return None

    def load_fermentables(self) -> Optional[pd.DataFrame]:
        """Load detailed fermentables data"""
        filepath = self.data_dir / "fermentables_detailed.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            fermentables_list = data.get("fermentables", [])
            if fermentables_list:
                return pd.DataFrame(fermentables_list)
        return None

    def load_beer_styles(self) -> Optional[pd.DataFrame]:
        """Load detailed beer styles with BJCP guidelines"""
        filepath = self.data_dir / "beer_styles_detailed.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            styles_list = data.get("styles", [])
            if styles_list:
                return pd.DataFrame(styles_list)
        return None

    def load_recipes(self) -> Optional[pd.DataFrame]:
        """Load advanced recipes data"""
        filepath = self.data_dir / "recipes_advanced.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            recipes_list = data.get("recipes", [])
            if recipes_list:
                return pd.DataFrame(recipes_list)
        return None

    def load_search_options(self) -> dict:
        """Load available search/filter options"""
        filepath = self.data_dir / "search_options.json"
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f)
        return {"search_options": {}}

    # ==================== ADVANCED FILTERING ====================

    def filter_recipes(
        self,
        style: Optional[str] = None,
        ibu_min: Optional[int] = None,
        ibu_max: Optional[int] = None,
        abv_min: Optional[float] = None,
        abv_max: Optional[float] = None,
        color_min: Optional[int] = None,
        color_max: Optional[int] = None,
        og_min: Optional[float] = None,
        og_max: Optional[float] = None,
        hops: Optional[list] = None,
        yeasts: Optional[list] = None,
        grains: Optional[list] = None,
    ) -> pd.DataFrame:
        """Advanced recipe filtering with multiple criteria"""
        recipes = self.load_recipes()
        if recipes is None or recipes.empty:
            return pd.DataFrame()

        filtered = recipes.copy()

        if style:
            filtered = filtered[
                filtered["style"].str.lower().str.contains(style.lower(), na=False)
            ]
        if ibu_min is not None:
            filtered = filtered[filtered["ibu"] >= ibu_min]
        if ibu_max is not None:
            filtered = filtered[filtered["ibu"] <= ibu_max]
        if abv_min is not None:
            filtered = filtered[filtered["abv"] >= abv_min]
        if abv_max is not None:
            filtered = filtered[filtered["abv"] <= abv_max]
        if color_min is not None:
            filtered = filtered[filtered["color"] >= color_min]
        if color_max is not None:
            filtered = filtered[filtered["color"] <= color_max]
        if og_min is not None:
            filtered = filtered[filtered["og"] >= og_min]
        if og_max is not None:
            filtered = filtered[filtered["og"] <= og_max]

        if hops:
            filtered = filtered[
                filtered["hops"].apply(
                    lambda x: any(h.lower() in str(x).lower() for h in hops)
                )
            ]
        if yeasts:
            filtered = filtered[filtered["yeast"].isin(yeasts)]
        if grains:
            filtered = filtered[
                filtered["grains"].apply(
                    lambda x: any(g.lower() in str(x).lower() for g in grains)
                )
            ]

        return filtered

    def filter_hops(
        self,
        alpha_acids_min: Optional[float] = None,
        alpha_acids_max: Optional[float] = None,
        origin: Optional[str] = None,
        purpose: Optional[str] = None,
        flavor: Optional[str] = None,
    ) -> pd.DataFrame:
        """Filter hops by characteristics"""
        hops = self.load_hops()
        if hops is None or hops.empty:
            return pd.DataFrame()

        filtered = hops.copy()

        if alpha_acids_min is not None:
            filtered = filtered[filtered["alpha_acids"] >= alpha_acids_min]
        if alpha_acids_max is not None:
            filtered = filtered[filtered["alpha_acids"] <= alpha_acids_max]
        if origin:
            filtered = filtered[
                filtered["origin"].str.lower().str.contains(origin.lower(), na=False)
            ]
        if purpose:
            filtered = filtered[
                filtered["purpose"].str.lower().str.contains(purpose.lower(), na=False)
            ]
        if flavor:
            filtered = filtered[
                filtered["flavor_profile"]
                .str.lower()
                .str.contains(flavor.lower(), na=False)
            ]

        return filtered

    def filter_yeasts(
        self,
        yeast_type: Optional[str] = None,
        temp_min: Optional[float] = None,
        temp_max: Optional[float] = None,
        attenuation_min: Optional[float] = None,
        flocculation: Optional[str] = None,
    ) -> pd.DataFrame:
        """Filter yeasts by characteristics"""
        yeasts = self.load_yeasts()
        if yeasts is None or yeasts.empty:
            return pd.DataFrame()

        filtered = yeasts.copy()

        if yeast_type:
            filtered = filtered[
                filtered["type"].str.lower().str.contains(yeast_type.lower(), na=False)
            ]
        if temp_min is not None:
            filtered = filtered[filtered["temperature_min"] >= temp_min]
        if temp_max is not None:
            filtered = filtered[filtered["temperature_max"] <= temp_max]
        if attenuation_min is not None:
            filtered = filtered[filtered["attenuation_min"] >= attenuation_min]
        if flocculation:
            filtered = filtered[
                filtered["flocculation"].str.lower()
                == flocculation.lower()
            ]

        return filtered

    def filter_fermentables(
        self,
        grain_type: Optional[str] = None,
        color_min: Optional[int] = None,
        color_max: Optional[int] = None,
        ppg_min: Optional[float] = None,
    ) -> pd.DataFrame:
        """Filter fermentables by type and properties"""
        fermentables = self.load_fermentables()
        if fermentables is None or fermentables.empty:
            return pd.DataFrame()

        filtered = fermentables.copy()

        if grain_type:
            filtered = filtered[
                filtered["type"].str.lower().str.contains(grain_type.lower(), na=False)
            ]
        if color_min is not None:
            filtered = filtered[filtered["color"] >= color_min]
        if color_max is not None:
            filtered = filtered[filtered["color"] <= color_max]
        if ppg_min is not None:
            filtered = filtered[filtered["ppg"] >= ppg_min]

        return filtered

    # ==================== ANALYTICS & STATISTICS ====================

    def get_style_guidelines(self, style_name: str) -> Optional[dict]:
        """Get detailed guidelines for a specific beer style"""
        styles = self.load_beer_styles()
        if styles is None or styles.empty:
            return None

        style = styles[
            styles["name"].str.lower() == style_name.lower()
        ].iloc[0]
        return style.to_dict()

    def get_hop_pairings(self, hop_name: str) -> list:
        """Get hops that pair well with a specific hop"""
        hops = self.load_hops()
        if hops is None or hops.empty:
            return []

        hop = hops[hops["name"].str.lower() == hop_name.lower()]
        if hop.empty:
            return []

        if "pairs_well_with" in hop.columns:
            pairs = hop.iloc[0]["pairs_well_with"]
            return pairs if isinstance(pairs, list) else []
        return []

    def get_recipes_by_style(self, style: str, limit: int = 20) -> pd.DataFrame:
        """Get popular recipes for a beer style"""
        recipes = self.load_recipes()
        if recipes is None or recipes.empty:
            return pd.DataFrame()

        filtered = recipes[
            recipes["style"].str.lower().str.contains(style.lower(), na=False)
        ]
        return filtered.nlargest(limit, "rating") if "rating" in filtered.columns else filtered.head(limit)

    def get_recommended_hops(self, style: str) -> list:
        """Get recommended hops for a beer style"""
        styles = self.load_beer_styles()
        if styles is None or styles.empty:
            return []

        style_data = styles[styles["name"].str.lower() == style.lower()]
        if style_data.empty:
            return []

        if "recommended_hops" in style_data.columns:
            return style_data.iloc[0]["recommended_hops"] or []
        return []

    def get_recommended_yeasts(self, style: str) -> list:
        """Get recommended yeasts for a beer style"""
        styles = self.load_beer_styles()
        if styles is None or styles.empty:
            return []

        style_data = styles[styles["name"].str.lower() == style.lower()]
        if style_data.empty:
            return []

        if "recommended_yeasts" in style_data.columns:
            return style_data.iloc[0]["recommended_yeasts"] or []
        return []

    def get_popular_hops(self, limit: int = 10) -> pd.DataFrame:
        """Get most popular hops"""
        hops = self.load_hops()
        if hops is None or hops.empty:
            return pd.DataFrame()

        if "recipes" in hops.columns:
            return hops.nlargest(limit, "recipes")
        return hops.head(limit)

    def get_popular_yeasts(self, limit: int = 10) -> pd.DataFrame:
        """Get most popular yeasts"""
        yeasts = self.load_yeasts()
        if yeasts is None or yeasts.empty:
            return pd.DataFrame()

        if "recipes" in yeasts.columns:
            return yeasts.nlargest(limit, "recipes")
        return yeasts.head(limit)

    def get_popular_grains(self, limit: int = 10) -> pd.DataFrame:
        """Get most popular grains"""
        fermentables = self.load_fermentables()
        if fermentables is None or fermentables.empty:
            return pd.DataFrame()

        if "recipes" in fermentables.columns:
            return fermentables.nlargest(limit, "recipes")
        return fermentables.head(limit)

    # ==================== STATISTICS ====================

    def get_recipe_statistics(self) -> dict:
        """Get overall recipe statistics"""
        recipes = self.load_recipes()
        if recipes is None or recipes.empty:
            return {}

        stats = {
            "total_recipes": len(recipes),
            "avg_ibu": recipes["ibu"].mean() if "ibu" in recipes.columns else 0,
            "avg_abv": recipes["abv"].mean() if "abv" in recipes.columns else 0,
            "avg_color": recipes["color"].mean() if "color" in recipes.columns else 0,
            "avg_og": recipes["og"].mean() if "og" in recipes.columns else 0,
            "ibu_range": (
                recipes["ibu"].min() if "ibu" in recipes.columns else 0,
                recipes["ibu"].max() if "ibu" in recipes.columns else 0,
            ),
            "abv_range": (
                recipes["abv"].min() if "abv" in recipes.columns else 0,
                recipes["abv"].max() if "abv" in recipes.columns else 0,
            ),
        }
        return stats

    def get_style_statistics(self) -> dict:
        """Get statistics by beer style"""
        recipes = self.load_recipes()
        if recipes is None or recipes.empty:
            return {}

        if "style" not in recipes.columns:
            return {}

        style_stats = {}
        for style in recipes["style"].unique():
            style_recipes = recipes[recipes["style"] == style]
            style_stats[style] = {
                "count": len(style_recipes),
                "avg_ibu": style_recipes["ibu"].mean() if "ibu" in style_recipes.columns else 0,
                "avg_abv": style_recipes["abv"].mean() if "abv" in style_recipes.columns else 0,
            }
        return style_stats

    def has_data(self) -> bool:
        """Check if data exists"""
        return any(
            (self.data_dir / f"{name}.json").exists()
            for name in [
                "hops_detailed",
                "yeasts_detailed",
                "beer_styles_detailed",
                "fermentables_detailed",
                "recipes_advanced",
            ]
        )
