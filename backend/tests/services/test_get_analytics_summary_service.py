from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.services.analytics.get_analytics_summary_service import GetAnalyticsSummaryService

FROM_TS = datetime(2024, 1, 1, tzinfo=timezone.utc)
TO_TS = datetime(2024, 12, 31, tzinfo=timezone.utc)


@pytest.mark.asyncio
async def test_summary_counts_events(db_session: AsyncSession):
    for action in ["carry", "carry", "unload"]:
        db_session.add(Event(
            camera_id="cam1", action_class=action, confidence=0.9,
            timestamp=datetime(2024, 6, 1, tzinfo=timezone.utc), metadata_={},
        ))
    await db_session.commit()

    summary = await GetAnalyticsSummaryService(db_session).execute(FROM_TS, TO_TS)

    assert summary.total_events == 3
    assert summary.events_by_class["carry"] == 2
    assert summary.events_by_class["unload"] == 1


@pytest.mark.asyncio
async def test_summary_empty_period(db_session: AsyncSession):
    summary = await GetAnalyticsSummaryService(db_session).execute(FROM_TS, TO_TS)

    assert summary.total_events == 0
    assert summary.avg_confidence == 0.0
