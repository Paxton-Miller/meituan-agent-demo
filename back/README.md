# Meituan Agent Tool Service

`back` is structured as a business API plus protocol adapters:

- `back/services/*`: protocol-independent domain logic.
- `back/api/routers/*`: REST and HTTP tool gateway.
- `back/agent_tools/*`: reusable tool definitions, schemas, registry, and adapters.
- `back/mcp_server.py`: MCP adapter for runtimes that can consume MCP tools.

## Run REST API

```bash
uvicorn main:app --reload --port 8000
```

Useful endpoints:

- `GET /api/v1/tools`: generic internal tool manifest.
- `GET /api/v1/tools/openai`: OpenAI function-tool definitions.
- `POST /api/v1/tools/call`: invoke a registered tool by name.
- `GET /docs`: FastAPI OpenAPI documentation.

Example tool call:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/tools/call \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: demo-001' \
  -d '{
    "name": "search_pois",
    "arguments": {
      "category": "ENTERTAINMENT",
      "tags": ["KIDS_FRIENDLY"]
    }
  }'
```

## OpenAI tools

```python
from back.agent_tools.adapters.openai_tools import to_openai_tools
from back.agent_tools.registry import registry

tools = to_openai_tools(registry)
result = await registry.invoke("get_user_context", {})
```

## LangChain

Install `langchain-core`, then:

```python
from back.agent_tools.adapters.langchain_tools import to_langchain_tools

tools = to_langchain_tools()
```

## MCP

Install the MCP Python package, then use one of these transports.

Stdio is best for local MCP clients that launch the server process:

```bash
python -m back.mcp_server
```

SSE is better when the MCP server runs as a long-lived network service:

```bash
python -m back.mcp_server --transport sse --host 127.0.0.1 --port 8001
```

SSE endpoints:

- `GET /sse`: MCP event stream.
- `POST /messages/`: client-to-server MCP messages.

Streamable HTTP is also available for clients that support the newer transport:

```bash
python -m back.mcp_server --transport streamable-http --host 127.0.0.1 --port 8001
```

Streamable HTTP endpoint:

- `/mcp`

The MCP server exports the same tools as the REST and OpenAI adapters.

## Production Notes

- Write tools such as `reserve_booking` are marked with `side_effect=True`.
- REST calls support `X-Request-ID`; booking also accepts `Idempotency-Key`.
- Services raise `ServiceError`, which adapters can map to HTTP status codes or agent runtime errors.
- The mock database is in memory. A production implementation should replace it with persistent storage, transactions, inventory locking, authentication, authorization, rate limiting, and audit logging.
