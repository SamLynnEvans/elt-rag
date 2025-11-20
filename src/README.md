### Simple MCP Server For Testing Integration With Claude

Add this config below to your MCP config file and you can experiment with how the semantic search will integrate with chat models like Claude.

```json
{
  "mcpServers": {
    "my-service": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "chroma_data:/app/chroma_store",
        "-e", "PYTHONUNBUFFERED=1",
        "-e", "GEMINI_API_KEY=your_actual_api_key_here",
        "-e", "CHROMA_DB_DIR=/app/chroma_store",
        "mcp-server:latest",
        "python", "-m", "mcp.app"
      ]
    }
  }
}
```
