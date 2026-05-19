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
| [journals.py](examples/python/journals.py) | Python | Create and list journal entries |
| [ask.py](examples/python/ask.py) | Python | RAG chat over campaign knowledge |
| [pagination.py](examples/python/pagination.py) | Python | Iterate through all pages of large collections |
| [error_handling.py](examples/python/error_handling.py) | Python | Retry logic, rate limits, error parsing |
| [types.ts](examples/typescript/types.ts) | TypeScript | Importable response type definitions |
| [curl/basics.sh](examples/curl/basics.sh) | cURL | Common operations as shell commands |

## API Base URL

```
https://api.myarchivist.ai
```

All endpoints require the `x-api-key` header for authentication.

## Resources

- [API Reference](https://developers.myarchivist.ai/api-reference)
- [Guides & Concepts](https://developers.myarchivist.ai/docs)
- [MCP Server](https://developers.myarchivist.ai/mcp)
- [Interactive Playground](https://developers.myarchivist.ai/playground)
- [Changelog](CHANGELOG.md)

## License

MIT
