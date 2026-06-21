"""bananaduck: a tiny LLM prompt router."""

from app.logging_setup import configure_sentry
from app.analytics import get_user_analytics


def main() -> None:
    configure_sentry()
    user_id = "demo-user"
    print(get_user_analytics(user_id))


if __name__ == "__main__":
    main()