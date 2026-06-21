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
    """Fetch DAU, MAU, and LTV for a user.

    Currently sequential. Should be parallelized in a follow-up.
    """
    dau = await fetch_metric("dau", user_id)
    mau = await fetch_metric("mau", user_id)
    ltv = await fetch_metric("ltv", user_id)
    return {"dau": dau, "mau": mau, "ltv": ltv}