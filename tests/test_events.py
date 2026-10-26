import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from events import (
    branch_from_ref,
    extract_issue_references,
    first_line,
    push_activity,
)


class EventTests(unittest.TestCase):
    def test_first_line(self):
        self.assertEqual(
            first_line("feat: add sync\n\nMore details"),
            "feat: add sync",
        )

    def test_branch_from_ref(self):
        self.assertEqual(
            branch_from_ref("refs/heads/feature/test"),
            "feature/test",
        )

    def test_issue_references_are_unique_and_sorted(self):
        self.assertEqual(
            extract_issue_references(
                "feat: work on #12 and #3, refs #12"
            ),
            [3, 12],
        )

    def test_push_activity(self):
        payload = {
            "ref": "refs/heads/main",
            "head_commit": {
                "message": "feat: sync project #12\nmore",
                "timestamp": "2026-10-26T12:00:00Z",
                "id": "abc123",
            },
        }

        self.assertEqual(
            push_activity(payload),
            {
                "message": "feat: sync project #12",
                "branch": "main",
                "timestamp": "2026-10-26T12:00:00Z",
                "sha": "abc123",
            },
        )


if __name__ == "__main__":
    unittest.main()
