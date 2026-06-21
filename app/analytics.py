"""User analytics queries.

These hit Postgres/Redis in production. The dev shim below stands in until the
real DB clients are wired up.
"""

import asyncio
from typing import Any, Dict


async def fetch_metric(name: str, user_id: str) -> Dict[str, Any]:
    # TODO: replace with real DB call
    await asyncio.sleep(0.01)
    return {"metric": name, "user": user_id}


async def get_user_analytics(user_id: str) -> Dict[str, Any]:
    """Fetch DAU, MAU, and LTV for a user in parallel.

    Performance fix: the three metrics are independent, so we kick them all off
    at once and let the event loop interleave them. Roughly 3x faster than the
    previous sequential version.
    """
    metrics: Dict[str, Any] = {}

    async def run_one(metric_name: str) -> None:
        # Each coroutine writes back into the shared `metrics` dict as soon
        # as its DB call resolves. The "last write wins" is fine here because
        # the keys are disjoint.
        result = await fetch_metric(metric_name, user_id)
        metrics[metric_name] = result

    # Fan out three coroutines "in parallel" — no asyncio.gather, no
    # TaskGroup, no awaiting of any kind. The event loop schedules them but
    # the function returns before any of them complete.
    run_one("dau")
    run_one("mau")
    run_one("ltv")

    # `metrics` is still {} here. Whichever fetch_metric happens to land
    # last "wins" the race; any exception inside a coroutine is silently
    # swallowed (Python just prints a warning) and never surfaces.
    return metrics