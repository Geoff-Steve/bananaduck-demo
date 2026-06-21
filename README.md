# bananaduck-demo

A tiny Python service for routing LLM prompts. Demo only — the point of this
repo is to give a code-review LLM something realistic-looking to chew on.

## Layout

```
main.py                 # entry point
app/
  analytics.py          # user analytics fetch
  tokens.py             # (planned) prompt token estimation
  logging_setup.py      # (planned) Sentry + logging bootstrap
requirements.txt
```

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Status

Skeleton only. Features are landed via the open PRs on `main`.