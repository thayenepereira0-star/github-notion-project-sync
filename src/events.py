import json
import re
from pathlib import Path
from typing import Any

ISSUE_REFERENCE_PATTERN = re.compile(r"(?<![\w/])#(\d+)\b")


def read_event_payload(event_path: str | None) -> dict[str, Any]:
    if not event_path:
        return {}

    path = Path(event_path)
    if not path.is_file():
        return {}

    with path.open(encoding="utf-8") as event_file:
        return json.load(event_file)


def first_line(message: str | None) -> str:
    if not message:
        return ""
    return message.strip().splitlines()[0][:2000]


def branch_from_ref(ref: str | None) -> str:
    if not ref:
        return ""

    prefix = "refs/heads/"
    return ref[len(prefix):] if ref.startswith(prefix) else ref


def extract_issue_references(message: str | None) -> list[int]:
    if not message:
        return []

    return sorted(
        {int(match) for match in ISSUE_REFERENCE_PATTERN.findall(message)}
    )


def push_activity(payload: dict[str, Any]) -> dict[str, str] | None:
    head_commit = payload.get("head_commit") or {}
    message = first_line(head_commit.get("message"))

    if not message:
        return None

    return {
        "message": message,
        "branch": branch_from_ref(payload.get("ref")),
        "timestamp": head_commit.get("timestamp") or "",
        "sha": head_commit.get("id") or "",
    }
