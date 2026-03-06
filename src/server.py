"""
MCP Server Template — Production-ready starting point.

Replace the example tools with your own. Each @mcp.tool() function
becomes a tool that AI agents (Claude, GPT, etc.) can call.

Run: python -m src.server
Test: mcp dev src/server.py
"""

import json
import os

from mcp.server.fastmcp import FastMCP
from src.api_client import api_get

# --- Server definition ---------------------------------------------------

mcp = FastMCP(
    "my-server",
    description="Short description of what your server provides to AI agents.",
)


# --- Tools ----------------------------------------------------------------
# Each tool = one function an AI agent can call.
# The docstring IS the description the agent reads. Make it specific.


@mcp.tool()
def get_status() -> str:
    """Get current system status: uptime, version, and health check results.
    Returns JSON with 'status', 'version', and 'checks' fields."""
    return json.dumps({
        "status": "healthy",
        "version": "1.0.0",
        "checks": {
            "database": "ok",
            "api": "ok",
            "cache": "ok",
        },
    }, indent=2)


@mcp.tool()
def search(query: str, limit: int = 10) -> str:
    """Search for items matching a query. Returns up to `limit` results
    with name, description, and score fields."""
    # Replace with your actual search logic
    data = api_get("/search", params={"q": query, "limit": limit})
    return json.dumps(data, indent=2)


@mcp.tool()
def get_item(item_id: str) -> str:
    """Get detailed information about a specific item by ID.
    Returns all fields including metadata and history."""
    data = api_get(f"/items/{item_id}")
    return json.dumps(data, indent=2)


@mcp.tool()
def compare(item_ids: str) -> str:
    """Compare two or more items side-by-side.
    Pass comma-separated IDs, e.g. 'abc,def,ghi'.
    Returns a comparison object with each item's key metrics."""
    ids = [i.strip() for i in item_ids.split(",")]
    results = {}
    for id in ids:
        results[id] = api_get(f"/items/{id}")
    return json.dumps(results, indent=2)


@mcp.tool()
def get_dashboard() -> str:
    """Get a combined overview: key metrics, active alerts, and recent
    activity in a single call. Saves the agent from making 3 separate requests."""
    return json.dumps({
        "metrics": api_get("/metrics"),
        "alerts": api_get("/alerts"),
        "recent": api_get("/activity?limit=5"),
    }, indent=2)


# --- Entry point ----------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
