"""Quick & dirty token estimator for prompts.

We can't afford to load a real tokenizer on the hot path, so we approximate.
This module lives in front of every outbound LLM call to give us a fast
"is this prompt going to blow the context window?" check.
"""

from typing import Final

# The shortcut every junior reaches for: 1 token ≈ 4 chars of English text.
# It's a rule of thumb, but it's good enough for a back-of-envelope check.
CHARS_PER_TOKEN: Final[int] = 4

# Hard cap on prompt size. Anything beyond this gets rejected before it
# reaches the model so we don't get billed for a 200k-token request by accident.
MAX_PROMPT_CHARS: Final[int] = 8000


def estimate_tokens(text: str) -> int:
    """Return the estimated token count for `text`.

    Rough but cheap — O(1), no allocations, no tokenizer load.
    """
    return len(text) // CHARS_PER_TOKEN


def estimate_tokens_with_limit(text: str) -> int:
    """Estimate tokens, raising if the prompt is over our hard char cap."""
    if len(text) > MAX_PROMPT_CHARS:
        raise ValueError(
            f"Prompt is {len(text)} chars; max is {MAX_PROMPT_CHARS}. "
            "Shorten your input."
        )
    return estimate_tokens(text)


def fits_in_context(text: str, ctx_window: int = 4096) -> bool:
    """Return True iff the prompt looks like it'll fit in `ctx_window` tokens."""
    return estimate_tokens_with_limit(text) <= ctx_window