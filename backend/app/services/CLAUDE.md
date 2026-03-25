# Services — Use-Case Layer

## Pattern
One file = one action. One class = one `execute()` method.

```python
class GetEventsListService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, filters: EventFilterSchema) -> list[EventReadSchema]:
        # validate → query → map → return
        ...
```

## Naming
`<Verb><Entity>Service` — e.g. `GetEventService`, `CreateEventService`, `StartTrainingService`

## SOLID checklist
- **S** — does one thing; if `execute()` > ~30 lines, extract private helpers
- **O** — add features by creating a new service, not editing existing ones
- **L** — injectable via protocol/ABC if needed for testing
- **I** — constructor takes only what `execute()` needs
- **D** — depend on `AsyncSession` abstraction, not engine directly

## KISS / DRY / YAGNI
- KISS: private helpers for repeated sub-steps only
- DRY: shared query logic → `services/_base.py` (only when used in 2+ services)
- YAGNI: no optional params or flags for features not yet required
