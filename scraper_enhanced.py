"""
Enhanced Firecrawl scraper for complete Beer Analytics data
Extracts all features: hops, yeasts, styles, fermentables, recipes, trends, pairings
"""

import json
import os
from pathlib import Path
from firecrawl import FirecrawlApp
import pandas as pd
from typing import Optional


class EnhancedBeerAnalyticsScraper:
    """Complete scraper for all Beer Analytics features"""

    def __init__(self, api_key: str | None = None):
        """Initialize enhanced Firecrawl scraper"""
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FIRECRAWL_API_KEY not set. "
                "Set it as environment variable or pass as parameter."
            )
        self.app = FirecrawlApp(api_key=self.api_key)
        self.base_url = "https://www.beer-analytics.com"

    def scrape_hops_detailed(self) -> dict:
        """Scrape comprehensive hop data with flavor profiles and pairings"""
        print("🌿 Scraping detailed hops data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/hops",
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
                                        "beta_acids": {"type": "number"},
                                        "cohumulone": {"type": "number"},
                                        "origin": {"type": "string"},
                                        "purpose": {"type": "string"},
                                        "aroma": {"type": "array", "items": {"type": "string"}},
                                        "flavor": {"type": "array", "items": {"type": "string"}},
                                        "flavor_profile": {"type": "string"},
                                        "recipes": {"type": "number"},
                                        "pairs_well_with": {"type": "array", "items": {"type": "string"}},
                                        "bittering_oz": {"type": "string"},
                                        "aroma_oz": {"type": "string"},
                                        "dry_hop_oz": {"type": "string"},
                                        "image_url": {"type": "string"},
                                    },
                                },
                            }
                        },
                    }
                },
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping hops: {e}")
            return {}

    def scrape_yeasts_detailed(self) -> dict:
        """Scrape comprehensive yeast data"""
        print("🧬 Scraping detailed yeasts data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/yeasts",
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
                                        "flavor_profile": {"type": "string"},
                                        "temperature_min": {"type": "number"},
                                        "temperature_max": {"type": "number"},
                                        "attenuation_min": {"type": "number"},
                                        "attenuation_max": {"type": "number"},
                                        "flocculation": {"type": "string"},
                                        "alcohol_tolerance": {"type": "number"},
                                        "recipes": {"type": "number"},
                                        "best_for": {"type": "array", "items": {"type": "string"}},
                                    },
                                },
                            }
                        },
                    }
                },
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping yeasts: {e}")
            return {}

    def scrape_fermentables_detailed(self) -> dict:
        """Scrape comprehensive fermentables/grains data"""
        print("🌾 Scraping detailed fermentables data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/fermentables",
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
                                        "flavor": {"type": "string"},
                                        "description": {"type": "string"},
                                        "recipes": {"type": "number"},
                                        "percentage_used": {"type": "number"},
                                        "typical_usage": {"type": "string"},
                                    },
                                },
                            }
                        },
                    }
                },
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping fermentables: {e}")
            return {}

    def scrape_beer_styles_detailed(self) -> dict:
        """Scrape comprehensive beer styles with guidelines"""
        print("🍻 Scraping detailed beer styles...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/beer-styles",
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
                                        "description": {"type": "string"},
                                        "origin": {"type": "string"},
                                        "ibu_min": {"type": "number"},
                                        "ibu_max": {"type": "number"},
                                        "abv_min": {"type": "number"},
                                        "abv_max": {"type": "number"},
                                        "color_min": {"type": "number"},
                                        "color_max": {"type": "number"},
                                        "og_min": {"type": "number"},
                                        "og_max": {"type": "number"},
                                        "fg_min": {"type": "number"},
                                        "fg_max": {"type": "number"},
                                        "overall_impression": {"type": "string"},
                                        "characteristic_flavors": {"type": "array", "items": {"type": "string"}},
                                        "recommended_hops": {"type": "array", "items": {"type": "string"}},
                                        "recommended_yeasts": {"type": "array", "items": {"type": "string"}},
                                        "typical_grains": {"type": "array", "items": {"type": "string"}},
                                        "recipes": {"type": "number"},
                                    },
                                },
                            }
                        },
                    }
                },
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping beer styles: {e}")
            return {}

    def scrape_recipes_advanced(self) -> dict:
        """Scrape comprehensive recipes with all details"""
        print("📋 Scraping detailed recipes...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}/recipes",
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
                                        "category": {"type": "string"},
                                        "ibu": {"type": "number"},
                                        "abv": {"type": "number"},
                                        "og": {"type": "number"},
                                        "fg": {"type": "number"},
                                        "color": {"type": "number"},
                                        "batch_size": {"type": "number"},
                                        "boil_size": {"type": "number"},
                                        "hops": {"type": "array", "items": {"type": "string"}},
                                        "grains": {"type": "array", "items": {"type": "string"}},
                                        "yeast": {"type": "string"},
                                        "difficulty": {"type": "string"},
                                        "rating": {"type": "number"},
                                        "brewer": {"type": "string"},
                                    },
                                },
                            }
                        },
                    }
                },
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping recipes: {e}")
            return {}

    def scrape_search_data(self) -> dict:
        """Scrape search/filter options"""
        print("🔍 Scraping search data...")
        try:
            result = self.app.scrape_url(
                f"{self.base_url}",
                {
                    "extractionSchema": {
                        "type": "object",
                        "properties": {
                            "search_options": {
                                "type": "object",
                                "properties": {
                                    "styles": {"type": "array", "items": {"type": "string"}},
                                    "hops": {"type": "array", "items": {"type": "string"}},
                                    "yeasts": {"type": "array", "items": {"type": "string"}},
                                    "fermentables": {"type": "array", "items": {"type": "string"}},
                                },
                            }
                        },
                    }
                },
            )
            return result.get("data", {})
        except Exception as e:
            print(f"Error scraping search data: {e}")
            return {}

    def save_data(self, data: dict, filename: str) -> None:
        """Save scraped data to JSON"""
        data_dir = Path("data/beer-analytics-full")
        data_dir.mkdir(parents=True, exist_ok=True)

        filepath = data_dir / filename
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved: {filepath}")


def scrape_all_complete(api_key: str | None = None) -> None:
    """Scrape ALL data from Beer Analytics"""
    scraper = EnhancedBeerAnalyticsScraper(api_key)

    print("\n" + "=" * 60)
    print("COMPREHENSIVE BEER ANALYTICS SCRAPE")
    print("=" * 60 + "\n")

    # Scrape all data
    data_sets = [
        ("hops_detailed.json", scraper.scrape_hops_detailed()),
        ("yeasts_detailed.json", scraper.scrape_yeasts_detailed()),
        ("fermentables_detailed.json", scraper.scrape_fermentables_detailed()),
        ("beer_styles_detailed.json", scraper.scrape_beer_styles_detailed()),
        ("recipes_advanced.json", scraper.scrape_recipes_advanced()),
        ("search_options.json", scraper.scrape_search_data()),
    ]

    for filename, data in data_sets:
        if data:
            scraper.save_data(data, filename)
        else:
            print(f"⚠️  No data for: {filename}")

    print("\n" + "=" * 60)
    print("✅ SCRAPING COMPLETE!")
    print("=" * 60 + "\n")
    print("Data saved to: data/beer-analytics-full/")


if __name__ == "__main__":
    scrape_all_complete()
