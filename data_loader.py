"""
Data loader for Beer Analytics scraped data
Provides convenient access to hops, yeasts, styles, recipes, etc.
"""

import json
from pathlib import Path
from typing import Optional
import pandas as pd


class DataLoader:
    """Load and manage Beer Analytics data"""

    def __init__(self, data_dir: str = "data/beer-analytics"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_hops(self) -> Optional[pd.DataFrame]:
        """Load hops data"""
        filepath = self.data_dir / "hops.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            hops_list = data.get("hops", [])
            if hops_list:
                return pd.DataFrame(hops_list)
        return None

    def load_yeasts(self) -> Optional[pd.DataFrame]:
        """Load yeasts data"""
        filepath = self.data_dir / "yeasts.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            yeasts_list = data.get("yeasts", [])
            if yeasts_list:
                return pd.DataFrame(yeasts_list)
        return None

    def load_beer_styles(self) -> Optional[pd.DataFrame]:
        """Load beer styles data"""
        filepath = self.data_dir / "beer_styles.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            styles_list = data.get("styles", [])
            if styles_list:
                return pd.DataFrame(styles_list)
        return None

    def load_fermentables(self) -> Optional[pd.DataFrame]:
        """Load fermentables/grains data"""
        filepath = self.data_dir / "fermentables.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            fermentables_list = data.get("fermentables", [])
            if fermentables_list:
                return pd.DataFrame(fermentables_list)
        return None

    def load_recipes(self) -> Optional[pd.DataFrame]:
        """Load recipes data"""
        filepath = self.data_dir / "recipes.json"
        if filepath.exists():
            with open(filepath) as f:
                data = json.load(f)
            recipes_list = data.get("recipes", [])
            if recipes_list:
                return pd.DataFrame(recipes_list)
        return None

    def load_trends(self) -> dict:
        """Load trends data"""
        filepath = self.data_dir / "trends.json"
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f)
        return {}

    def has_scraped_data(self) -> bool:
        """Check if scraped data exists"""
        return any(
            (self.data_dir / f"{name}.json").exists()
            for name in ["hops", "yeasts", "beer_styles", "fermentables", "recipes"]
        )

    def get_recipes_by_style(self, style: str) -> pd.DataFrame:
        """Get recipes for a specific beer style"""
        recipes = self.load_recipes()
        if recipes is not None:
            return recipes[recipes["style"].str.lower() == style.lower()]
        return pd.DataFrame()

    def get_recipes_by_hop(self, hop: str) -> pd.DataFrame:
        """Get recipes using a specific hop"""
        recipes = self.load_recipes()
        if recipes is not None:
            return recipes[
                recipes["hops"].apply(lambda x: hop.lower() in str(x).lower())
            ]
        return pd.DataFrame()

    def get_popular_hops(self, limit: int = 10) -> pd.DataFrame:
        """Get most popular hops by usage count"""
        hops = self.load_hops()
        if hops is not None and "recipes" in hops.columns:
            return hops.nlargest(limit, "recipes")
        return pd.DataFrame()

    def get_popular_yeasts(self, limit: int = 10) -> pd.DataFrame:
        """Get most popular yeasts by usage count"""
        yeasts = self.load_yeasts()
        if yeasts is not None and "recipes" in yeasts.columns:
            return yeasts.nlargest(limit, "recipes")
        return pd.DataFrame()

    def search_recipes(
        self,
        style: Optional[str] = None,
        ibu_min: Optional[int] = None,
        ibu_max: Optional[int] = None,
        abv_min: Optional[float] = None,
        abv_max: Optional[float] = None,
    ) -> pd.DataFrame:
        """Search recipes with multiple filters"""
        recipes = self.load_recipes()
        if recipes is None:
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

        return filtered

    def get_hop_stats(self) -> dict:
        """Get statistics about hops"""
        hops = self.load_hops()
        if hops is None:
            return {}

        stats = {
            "total_hops": len(hops),
            "avg_alpha_acids": hops["alpha_acids"].mean() if "alpha_acids" in hops.columns else 0,
            "avg_recipes": hops["recipes"].mean() if "recipes" in hops.columns else 0,
        }
        return stats

    def get_recipe_stats(self) -> dict:
        """Get statistics about recipes"""
        recipes = self.load_recipes()
        if recipes is None:
            return {}

        stats = {
            "total_recipes": len(recipes),
            "avg_ibu": recipes["ibu"].mean() if "ibu" in recipes.columns else 0,
            "avg_abv": recipes["abv"].mean() if "abv" in recipes.columns else 0,
            "avg_color": recipes["color"].mean() if "color" in recipes.columns else 0,
        }
        return stats
