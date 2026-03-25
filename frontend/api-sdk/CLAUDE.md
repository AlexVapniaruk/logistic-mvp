# api-sdk — HTTP Contract Layer

Single responsibility: typed communication with the backend API.

## Files
| File | Purpose |
|---|---|
| `client.ts` | Base ofetch instance — base URL, default headers |
| `types.ts` | All TypeScript interfaces mirroring backend Pydantic schemas |
| `*.api.ts` | One file per backend router; exports typed async functions |
| `ws.client.ts` | WebSocket wrapper with reconnect logic and typed messages |

## Rules (SRP / ISP)
- No business logic — transform data only if the backend response shape is wrong
- No UI state — return raw typed data, let stores handle state
- Export named functions, not classes
- All functions return `Promise<T>` using types from `types.ts`
- `types.ts` is the single source of truth for API shapes
