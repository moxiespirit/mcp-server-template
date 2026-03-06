"""
Minimal example: Weather API as MCP tools.

Shows the simplest possible MCP server -- 2 tools wrapping a public API.
Run: python examples/weather_server.py
"""

import json
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather", description="Current weather and forecasts for any city.")
client = httpx.Client(timeout=10)

# Free API, no key needed for demo
API_URL = "https://wttr.in"


@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city. Returns temperature, conditions,
    humidity, and wind speed."""
    resp = client.get(f"{API_URL}/{city}?format=j1")
    resp.raise_for_status()
    data = resp.json()
    current = data["current_condition"][0]
    return json.dumps({
        "city": city,
        "temp_f": current["temp_F"],
        "temp_c": current["temp_C"],
        "conditions": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"],
        "wind_mph": current["windspeedMiles"],
    }, indent=2)


@mcp.tool()
def get_forecast(city: str, days: int = 3) -> str:
    """Get weather forecast for a city. Returns high/low temps and
    conditions for each day. Max 3 days."""
    resp = client.get(f"{API_URL}/{city}?format=j1")
    resp.raise_for_status()
    data = resp.json()
    forecast = []
    for day in data["weather"][:days]:
        forecast.append({
            "date": day["date"],
            "high_f": day["maxtempF"],
            "low_f": day["mintempF"],
            "conditions": day["hourly"][4]["weatherDesc"][0]["value"],
        })
    return json.dumps({"city": city, "forecast": forecast}, indent=2)


if __name__ == "__main__":
    mcp.run()
