"""
Firecrawl scraper for Beer Analytics data
Extracts beer styles, hops, yeasts, and recipe data
"""

import json
import os
from pathlib import Path
from firecrawl import FirecrawlApp
import pandas as pd


class BeerAnalyticsScraper:
    """Scrapes data from Beer Analytics using Firecrawl"""

    def __init__(self, api_key: str | None = None):
        """Initialize Firecrawl scraper"""
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FIRECRAWL_API_KEY not set. "
                "Set it as environment variable or pass as parameter."
            )
        self.app = FirecrawlApp(api_key=self.api_key)
        self.base_url = "https://www.beer-analytics.com"

    def scrape_hops(self) -> dict:
        """Scrape hop varieties and their characteristics"""
        print("Scraping hops data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/hops",
                {"extractionSchema": self._get_hops_schema()},
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping hops: {e}")
            return {}

    def scrape_yeasts(self) -> dict:
        """Scrape yeast strains and their properties"""
        print("Scraping yeasts data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/yeasts",
                {"extractionSchema": self._get_yeasts_schema()},
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping yeasts: {e}")
            return {}

    def scrape_beer_styles(self) -> dict:
        """Scrape beer styles and guidelines"""
        print("Scraping beer styles...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/beer-styles",
                {"extractionSchema": self._get_styles_schema()},
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping beer styles: {e}")
            return {}

    def scrape_fermentables(self) -> dict:
        """Scrape grains and fermentables"""
        print("Scraping fermentables data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/fermentables",
                {"extractionSchema": self._get_fermentables_schema()},
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping fermentables: {e}")
            return {}

    def scrape_recipes(self, filters: dict | None = None) -> list:
        """Scrape recipes with optional filters"""
        print("Scraping recipes...")
        try:
            url = f"{self.base_url}/recipes"
            if filters:
                query_params = "&".join([f"{k}={v}" for k, v in filters.items()])
                url = f"{url}?{query_params}"

            result = self.app.scrape_url(
                url, {"extractionSchema": self._get_recipes_schema()}
            )
            return result.get("data", {}).get("recipes", [])
        except Exception as e:
            print(f"Error scraping recipes: {e}")
            return []

    def scrape_trends(self) -> dict:
        """Scrape trending recipes and hops"""
        print("Scraping trends data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/trends",
                {"extractionSchema": self._get_trends_schema()},
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping trends: {e}")
            return {}

    @staticmethod
    def _get_hops_schema() -> dict:
        """Schema for hop extraction"""
        return {
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
                            "aroma": {"type": "string"},
                            "flavor": {"type": "string"},
                            "recipes": {"type": "number"},
                        },
                    },
                }
            },
        }

    @staticmethod
    def _get_yeasts_schema() -> dict:
        """Schema for yeast extraction"""
        return {
            "type": "object",
            "properties": {
                "yeasts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "flavor_profile": {"type": "string"},
                            "temperature_range": {"type": "string"},
                            "attenuation": {"type": "number"},
                            "recipes": {"type": "number"},
                        },
                    },
                }
            },
        }

    @staticmethod
    def _get_styles_schema() -> dict:
        """Schema for beer styles extraction"""
        return {
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
                            "description": {"type": "string"},
                        },
                    },
                }
            },
        }

    @staticmethod
    def _get_fermentables_schema() -> dict:
        """Schema for fermentables extraction"""
        return {
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
                            "flavor": {"type": "string"},
                            "recipes": {"type": "number"},
                        },
                    },
                }
            },
        }

    @staticmethod
    def _get_recipes_schema() -> dict:
        """Schema for recipes extraction"""
        return {
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
                            "hops": {"type": "array", "items": {"type": "string"}},
                            "grains": {"type": "array", "items": {"type": "string"}},
                            "yeast": {"type": "string"},
                        },
                    },
                }
            },
        }

    @staticmethod
    def _get_trends_schema() -> dict:
        """Schema for trends extraction"""
        return {
            "type": "object",
            "properties": {
                "trending_hops": {"type": "array", "items": {"type": "string"}},
                "trending_styles": {"type": "array", "items": {"type": "string"}},
                "trending_recipes": {
                    "type": "array",
                    "items": {"type": "object"},
                },
            },
        }

    def save_data(self, data: dict, filename: str) -> None:
        """Save scraped data to JSON file"""
        data_dir = Path("data/beer-analytics")
        data_dir.mkdir(parents=True, exist_ok=True)

        filepath = data_dir / filename
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved data to {filepath}")

    def load_data(self, filename: str) -> dict:
        """Load scraped data from JSON file"""
        filepath = Path("data/beer-analytics") / filename
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f)
        return {}


def scrape_and_save_all(api_key: str | None = None) -> None:
    """Scrape all data from Beer Analytics and save locally"""
    scraper = BeerAnalyticsScraper(api_key)

    # Scrape and save each data type
    hops_data = scraper.scrape_hops()
    if hops_data:
        scraper.save_data(hops_data, "hops.json")

    yeasts_data = scraper.scrape_yeasts()
    if yeasts_data:
        scraper.save_data(yeasts_data, "yeasts.json")

    styles_data = scraper.scrape_beer_styles()
    if styles_data:
        scraper.save_data(styles_data, "beer_styles.json")

    fermentables_data = scraper.scrape_fermentables()
    if fermentables_data:
        scraper.save_data(fermentables_data, "fermentables.json")

    recipes_data = scraper.scrape_recipes()
    if recipes_data:
        scraper.save_data({"recipes": recipes_data}, "recipes.json")

    trends_data = scraper.scrape_trends()
    if trends_data:
        scraper.save_data(trends_data, "trends.json")

    print("\n✅ All data scraped and saved!")


if __name__ == "__main__":
    # Run: python scraper_firecrawl.py
    # Make sure FIRECRAWL_API_KEY is set in environment
    scrape_and_save_all()
