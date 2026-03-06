FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir -e .

# For stdio transport (Claude Desktop), the CMD isn't used.
# For HTTP transport (remote deployment), uncomment:
# CMD ["uvicorn", "src.server:mcp.app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["python", "-m", "src.server"]
