import os
import requests
from typing import Any, Dict


def get_weather(city: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing OPENWEATHER_API_KEY in environment. Add it to your .env file."
        )

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}"
    )

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

