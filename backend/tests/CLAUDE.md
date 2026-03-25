# Tests — FIRST Principles

## Rules
| Principle | How |
|---|---|
| **Fast** | aiosqlite in-memory DB — no network, no docker |
| **Isolated** | Function-scoped `AsyncSession`, rolled back after each test |
| **Repeatable** | `faker` with fixed seed; no shared mutable state between tests |
| **Self-validating** | `assert` only — no `print`, no manual inspection |
| **Timely** | Written alongside the service, not after the fact |

## Structure mirrors `app/`
```
tests/services/   ↔   app/services/
tests/routers/    ↔   app/routers/
tests/conftest.py     shared fixtures only
```

## Fixture rules
- All fixtures in `conftest.py` — no local fixture duplication
- DB fixture: `AsyncSession` over in-memory SQLite, `function` scope
- HTTP fixture: `AsyncClient` with `ASGITransport` (httpx), `function` scope
- Mock redis with `unittest.mock.AsyncMock`

## Run
```bash
pytest tests/ -v
```
