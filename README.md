# MCP Server Template

A production-ready template for building [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) servers in Python using [FastMCP](https://github.com/jlowin/fastmcp).

MCP is the open standard by Anthropic that lets AI agents (Claude, GPT, custom LLMs) access external tools and data sources through a unified protocol.

## What's Included

```
src/
  server.py          # MCP server with example tools
  api_client.py      # HTTP client wrapper (connect to any REST API)
examples/
  weather_server.py  # Minimal example: weather API tools
  database_server.py # Example: database query tools
Dockerfile           # Production deployment
pyproject.toml       # Package config (pip-installable)
claude_config.json   # Claude Desktop integration config
```

## Quick Start

### 1. Install

```bash
pip install -e .
```

### 2. Run locally

```bash
python -m src.server
```

### 3. Connect to Claude Desktop

Copy `claude_config.json` into your Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/this/repo"
    }
  }
}
```

Restart Claude Desktop. Your tools will appear in the tool picker.

## Building Your Own Server

### Step 1: Define your tools

Edit `src/server.py`. Each tool is a decorated function:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server", description="What my server does.")

@mcp.tool()
def get_data(query: str) -> str:
    """Tool description that the AI agent sees. Be specific about what it returns."""
    result = your_api_call(query)
    return json.dumps(result, indent=2)
```

**Tool design tips:**
- The docstring IS the tool description. Agents read it to decide when to call your tool.
- Return JSON strings for structured data.
- Keep tools focused: one tool = one action.
- Use clear parameter names and type hints.

### Step 2: Connect to your data source

Edit `src/api_client.py` to point at your API:

```python
BASE_URL = os.environ.get("MY_API_URL", "https://api.example.com")
API_KEY = os.environ.get("MY_API_KEY", "")
```

### Step 3: Deploy

**Docker (Railway, Fly.io, AWS):**
```bash
docker build -t my-mcp-server .
docker run -p 8000:8000 my-mcp-server
```

**Direct:**
```bash
pip install -e .
my-mcp-server  # runs the console script
```

## Tool Patterns

### Wrapping a REST API
```python
@mcp.tool()
def search_products(query: str, limit: int = 10) -> str:
    """Search the product catalog. Returns name, price, and availability."""
    data = client.get("/products", params={"q": query, "limit": limit})
    return json.dumps(data, indent=2)
```

### Querying a database
```python
@mcp.tool()
def get_user_orders(user_id: str) -> str:
    """Get recent orders for a user. Returns order ID, date, total, and status."""
    rows = db.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY date DESC LIMIT 20", [user_id])
    return json.dumps([dict(r) for r in rows], indent=2)
```

### Aggregating multiple sources
```python
@mcp.tool()
def get_dashboard() -> str:
    """Get a combined dashboard: metrics, alerts, and recent activity in one call."""
    return json.dumps({
        "metrics": get_metrics(),
        "alerts": get_active_alerts(),
        "recent": get_recent_activity(limit=5),
    }, indent=2)
```

### Parameterized comparison
```python
@mcp.tool()
def compare_items(item_ids: str) -> str:
    """Compare two or more items side-by-side. Pass comma-separated IDs, e.g. 'abc,def'."""
    ids = [i.strip() for i in item_ids.split(",")]
    results = {id: get_item(id) for id in ids}
    return json.dumps(results, indent=2)
```

## Production Checklist

- [ ] Every tool has a clear, specific docstring
- [ ] All API keys are in environment variables (never hardcoded)
- [ ] HTTP client has timeouts set (`httpx.Client(timeout=15)`)
- [ ] Error responses return helpful messages, not stack traces
- [ ] Tools return JSON strings for structured data
- [ ] Dockerfile builds and runs cleanly
- [ ] `pyproject.toml` has correct entry point
- [ ] Tested with Claude Desktop or `mcp dev` before deploying

## Testing

```bash
# Run the MCP development inspector
mcp dev src/server.py

# Or test tools directly
python -c "from src.server import get_status; print(get_status())"
```

## Real-World Examples

This template is extracted from production MCP servers:

- **[OathScore](https://github.com/moxiespirit/oathscore)** — 8 tools: real-time exchange status, volatility data, economic events, API quality scoring. Serves AI trading agents.
- **Curistat** — 10 tools: volatility forecasting, regime detection, directional signals. Production with paying subscribers.

## License

MIT
