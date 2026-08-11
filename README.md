# Meeting Miner

> Offline meeting → actions/decisions

**Author:** zAx4hub

## Problem

Meeting transcripts bury decisions and action items in chatty prose. Teams need an offline extractor that works without an LLM API.

## Solution

`meeting-miner` parses speaker lines and extracts action items, owners, and decisions with deterministic patterns — then summarizes the meeting.

## Why different

- Fully offline / regex+structure based
- Owner detection from several phrasings
- Deterministic fixtures and tests
- Owned and credited to **zAx4hub**

## Quickstart

```bash
cd meeting-miner
pip install -e ".[dev]"
pytest -q
meeting-miner demo
```

## Features

- Speaker/transcript parsing
- ACTION/TODO/`will` extraction
- DECISION / “we agreed” extraction
- Owner attribution
- Summary metrics

## Architecture

Pure extraction in `src/meeting_miner/engine.py`; CLI is a thin wrapper.

## Contributing

PRs welcome — keep changes focused and add tests.

## Credits

Built and maintained by **zAx4hub**.

## License

MIT © 2026 zAx4hub
