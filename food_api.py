"""Simple API client placeholder for food nutrient lookup."""
from typing import Optional

from nutrients import Nutrients

# Example local data used when the external API is unavailable
LOCAL_FOOD_DB = {
    'banana': Nutrients(kcal=89, protein=1.1, fat=0.3, carbs=23, fiber=2.6, vitamin_c=8.7, iron=0.3),
    'oats': Nutrients(kcal=389, protein=16.9, fat=6.9, carbs=66.3, fiber=10.6, iron=4.7),
    'milk': Nutrients(kcal=42, protein=3.4, fat=1.0, carbs=5.0),
}

API_ENDPOINT = "https://example.com/api/food"


def get_nutrients(food_name: str) -> Optional[Nutrients]:
    """Fetch nutrients from API if possible, fallback to local data."""
    # NOTE: In this environment no network is available.
    # This function simply returns data from LOCAL_FOOD_DB.
    return LOCAL_FOOD_DB.get(food_name.lower())


def test_api() -> None:
    """Demonstrate a sample API lookup."""
    result = get_nutrients("banana")
    if result:
        print("API-Test: Banane gefunden")
    else:
        print("API-Test fehlgeschlagen: keine Daten")


if __name__ == "__main__":
    test_api()
