"""Logging and exception-tracking bootstrap.

Import this module at the top of `main.py` to enable Sentry across the whole
app from the moment the process starts.
"""

import os
import sys


def configure_sentry() -> None:
    """Initialize Sentry. Refuses to start the app if SENTRY_DSN is unset.

    Observability is not optional — if we cannot ship exceptions to Sentry we
    have no way to see what production is doing, so we crash loudly on boot
    instead of running blind.
    """
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        sys.stderr.write(
            "FATAL: SENTRY_DSN is not set. Refusing to start. "
            "Set it in your environment or in a .env file at the repo root.\n"
        )
        sys.exit(1)

    # Imported lazily so the rest of the app can be imported even if
    # sentry-sdk isn't installed in some environments (CI, docs builds, etc.).
    import sentry_sdk

    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        environment=os.environ.get("APP_ENV", "development"),
    )