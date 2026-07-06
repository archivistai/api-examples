# Archivist API Examples

Code examples and usage patterns for the [Archivist AI](https://myarchivist.ai) public REST API.

## Getting Started

1. Create an API key at [app.myarchivist.ai/profile?section=dev](https://app.myarchivist.ai/profile?section=dev)
2. Set your key as an environment variable:
   ```bash
   export ARCHIVIST_API_KEY="your-api-key-here"
   ```
3. Browse the examples below or explore the [full API reference](https://developers.myarchivist.ai/api-reference)

## Examples

| Example | Language | Description |
|---------|----------|-------------|
| [quickstart.py](examples/python/quickstart.py) | Python | List campaigns, characters, and sessions |
| [quickstart.ts](examples/typescript/quickstart.ts) | TypeScript | Same flow using fetch |
| [quests.py](examples/python/quests.py) | Python | Create and manage quests |
| [beats.py](examples/python/beats.py) | Python | Fetch nested session beat hierarchy |
| [entities.py](examples/python/entities.py) | Python | Unified compendium entity picker |
| [moments.py](examples/python/moments.py) | Python | Moment list filters and fields=card |
| [journals.py](examples/python/journals.py) | Python | List journal entries with pagination and fields=card |
| [ask.py](examples/python/ask.py) | Python | RAG chat over campaign knowledge |
| [pagination.py](examples/python/pagination.py) | Python | Iterate standard and entities list envelopes |
| [images.py](examples/python/images.py) | Python | Image quota, AI generation, and direct upload init |
| [error_handling.py](examples/python/error_handling.py) | Python | Retry logic, rate limits, error parsing |
| [types.ts](examples/typescript/types.ts) | TypeScript | Importable response type definitions |
| [curl/basics.sh](examples/curl/basics.sh) | cURL | Common operations as shell commands |

## API Base URL

```
https://api.myarchivist.ai
```

All endpoints require the `x-api-key` header for authentication.

## Response envelopes

Most list endpoints return the **standard pagination envelope**:

```json
{ "data": [...], "total": 42, "page": 1, "size": 20, "pages": 3 }
```

Use `page` and `size` query parameters to paginate. Examples: `/v1/characters`, `/v1/moments`, `/v1/journals`.

**`GET /v1/entities`** uses a different envelope suited to pickers:

```json
{ "results": [...], "hasMore": true, "page": 1, "pages": 5, "total": 42 }
```

Use `page` and `limit` (not `size`) to paginate. Each result includes `id`, `name`, `type`, and `image`.

**Session beats** — `GET /v1/beats?session_id={id}` returns a paginated flat list of beats linked to that session. Add `include_hierarchy=true` for a nested JSON array (not paginated); each node includes a `children` array.

**`fields=card`** on `GET /v1/characters`, `GET /v1/moments`, and `GET /v1/journals` returns lightweight list items for pickers and feeds instead of full summaries.

## Resources

- [API Reference](https://developers.myarchivist.ai/api-reference)
- [Guides & Concepts](https://developers.myarchivist.ai/docs)
- [MCP Server](https://developers.myarchivist.ai/mcp)
- [Interactive Playground](https://developers.myarchivist.ai/playground)
- [Changelog](CHANGELOG.md)

## License

MIT
