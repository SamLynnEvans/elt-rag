import os

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
import chromadb
import google.generativeai as genai


app = Server("policy-search")


client = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH"))


collection = client.get_or_create_collection(
    name="policy_rag",
    metadata={"hnsw:space": "cosine"}
)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of strings using Gemini embeddings."""

    response = genai.embed_content(
        model="gemini-embedding-001",
        content=texts
    )

    return response['embedding']


def search(query: str, top_k: int = 1, where: dict | None = None) -> list[str]:
    embedding = embed_texts([query])[0]

    result = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        where=where
    )

    return result["documents"][0]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="Policy Semantic Search",
            description="Embeds queries and performs semantic search for relevant policy documents.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for relevant policy documents."
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "Policy Semantic Search":
        # Your service logic here
        result = search(arguments["param1"])
        return [TextContent(type="text", text=str(result))]

    raise ValueError(f"Unknown tool: {name}")


if __name__ == "__main__":
    import app.server.stdio
    mcp.server.stdio.run(app)