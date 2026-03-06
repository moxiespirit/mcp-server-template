"""
Example: SQLite database exposed as MCP tools.

Shows how to give AI agents read access to a database.
Run: python examples/database_server.py
"""

import json
import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("database", description="Query the application database.")

DB_PATH = "example.db"


def _query(sql: str, params: list | None = None) -> list[dict]:
    """Execute a read-only query and return rows as dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql, params or []).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@mcp.tool()
def list_tables() -> str:
    """List all tables in the database with their row counts."""
    tables = _query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    result = []
    for t in tables:
        count = _query(f"SELECT COUNT(*) as n FROM [{t['name']}]")
        result.append({"table": t["name"], "rows": count[0]["n"]})
    return json.dumps(result, indent=2)


@mcp.tool()
def describe_table(table_name: str) -> str:
    """Get column names and types for a table."""
    cols = _query(f"PRAGMA table_info([{table_name}])")
    return json.dumps([{"name": c["name"], "type": c["type"]} for c in cols], indent=2)


@mcp.tool()
def query_table(table_name: str, where: str = "", limit: int = 20) -> str:
    """Query rows from a table. Optional WHERE clause (without the WHERE keyword).
    Example: query_table('users', where='age > 30', limit=10)"""
    sql = f"SELECT * FROM [{table_name}]"
    if where:
        sql += f" WHERE {where}"
    sql += f" LIMIT {limit}"
    rows = _query(sql)
    return json.dumps(rows, indent=2)


if __name__ == "__main__":
    mcp.run()
