"""kms_mcp — MCP server exposing this knowledge repo as a Kuzu knowledge graph
with local semantic search.

Layers:
- content.py    parse nuggets/, wiki/, sources/, graph/entities.yaml
- embeddings.py local sentence embeddings (all-MiniLM-L6-v2 via fastembed/ONNX)
- indexer.py    build the Kuzu database under .kms-index/
- search.py     in-memory cosine search over embeddings stored in the graph
- server.py     FastMCP tools (stdio + streamable HTTP)
"""

__version__ = "0.1.0"
