"""meeting-miner — offline meeting → actions/decisions by zAx4hub."""
from __future__ import annotations

import re
from typing import Any

AUTHOR = "zAx4hub"

SPEAKER_RE = re.compile(r"^([A-Za-z][\w.\- ]{0,40}):\s*(.+)$")
ACTION_PREFIX = re.compile(r"(?i)^(?:[-*]|\d+[.)])?\s*(?:TODO|ACTION|AI|follow[- ]?up)\s*[:\-]\s*(.+)$")
ACTION_OWNER = re.compile(r"(?i)^(?:[-*])?\s*(.+)\s+\((?:owner|assignee)\s*:\s*([^)]+)\)\s*$")
ACTION_WILL = re.compile(r"(?i)^([A-Z][a-z]+)\s+will\s+(.+)$")
ACTION_CHECK = re.compile(r"(?i)^(?:[-*]\s*)?\[\s\]\s*(.+)$")
DECISION_PREFIX = re.compile(r"(?i)^(?:[-*]|\d+[.)])?\s*(?:DECISION|DECIDED|WE AGREED)\s*[:\-]\s*(.+)$")
DECISION_SOFT = re.compile(r"(?i)\b(?:we|team)\s+(?:decided|agreed)\s+(?:to\s+)?(.+)$")


def parse_transcript(text: str) -> list[dict[str, str]]:
    lines: list[dict[str, str]] = []
    speaker = "unknown"
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = SPEAKER_RE.match(line)
        if m:
            speaker, content = m.group(1).strip(), m.group(2).strip()
            lines.append({"speaker": speaker, "text": content})
        else:
            lines.append({"speaker": speaker, "text": line})
    return lines


def extract_actions(lines: list[dict[str, str]]) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    for line in lines:
        text = line["text"]
        m = ACTION_PREFIX.match(text)
        if m:
            actions.append({"text": m.group(1).strip(), "owner": line["speaker"], "source": text})
            continue
        m = ACTION_OWNER.match(text)
        if m:
            actions.append({"text": m.group(1).strip(), "owner": m.group(2).strip(), "source": text})
            continue
        m = ACTION_WILL.match(text)
        if m:
            actions.append({"text": m.group(2).strip(), "owner": m.group(1).strip(), "source": text})
            continue
        m = ACTION_CHECK.match(text)
        if m:
            actions.append({"text": m.group(1).strip(), "owner": line["speaker"], "source": text})
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for a in actions:
        key = (a["text"].lower(), a["owner"].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(a)
    return out


def extract_decisions(lines: list[dict[str, str]]) -> list[dict[str, str]]:
    decisions: list[dict[str, str]] = []
    for line in lines:
        text = line["text"]
        m = DECISION_PREFIX.match(text) or DECISION_SOFT.search(text)
        if not m:
            continue
        body = m.group(1).strip()
        if body:
            decisions.append({"text": body, "speaker": line["speaker"]})
    return decisions


def summarize(lines: list[dict[str, str]], actions: list[dict[str, str]], decisions: list[dict[str, str]]) -> str:
    speakers = sorted({l["speaker"] for l in lines})
    return (
        f"{len(lines)} utterances by {', '.join(speakers)}; "
        f"{len(decisions)} decisions; {len(actions)} action items."
    )


def run(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    transcript = payload.get("transcript") or DEMO_TRANSCRIPT
    lines = parse_transcript(transcript)
    actions = extract_actions(lines)
    decisions = extract_decisions(lines)
    summary = summarize(lines, actions, decisions)
    return {
        "project": "meeting-miner",
        "author": AUTHOR,
        "summary": summary,
        "actions": actions,
        "decisions": decisions,
        "speakers": sorted({l["speaker"] for l in lines}),
        "metrics": {
            "lines": len(lines),
            "actions": len(actions),
            "decisions": len(decisions),
        },
    }


DEMO_TRANSCRIPT = """
Ada: Welcome everyone to the planning sync.
Ben: We decided to ship the beta on Friday.
Ada: ACTION: Ada will finalize the README.
Ben: TODO: Ben will fix the flaky CI job.
Cara: Cara will prepare demo scripts (owner: Cara).
Ada: [ ] Follow up with design on empty states
Ben: We agreed to keep the API backwards compatible.
"""


def demo() -> dict[str, Any]:
    return run({})


def inspect() -> dict[str, Any]:
    return {
        "name": "meeting-miner",
        "author": AUTHOR,
        "oneLiner": "Offline meeting → actions/decisions",
        "version": "0.1.0",
        "features": [
            "transcript parse",
            "action extraction",
            "decision extraction",
            "owner detection",
            "summary metrics",
        ],
    }
