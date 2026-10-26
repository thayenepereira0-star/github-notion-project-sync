import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from sync_service import (
    build_notion_properties,
    rich_text_property,
)


class SyncServiceTests(unittest.TestCase):
    def test_rich_text_property(self):
        self.assertEqual(
            rich_text_property("hello"),
            {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "hello"},
                    }
                ]
            },
        )

    def test_build_properties_with_activity(self):
        repository_data = {
            "html_url": "https://github.com/acme/demo",
            "default_branch": "main",
            "pushed_at": "2026-10-25T10:00:00Z",
        }
        activity = {
            "message": "feat: new pipeline",
            "branch": "feature/pipeline",
            "timestamp": "2026-10-26T10:00:00Z",
            "sha": "abc",
        }

        result = build_notion_properties(
            repository_data,
            activity,
        )

        self.assertEqual(
            result["Repositório GitHub"]["url"],
            "https://github.com/acme/demo",
        )
        self.assertEqual(
            result["Última atualização GitHub"]["date"]["start"],
            "2026-10-26T10:00:00Z",
        )
        self.assertEqual(
            result["Branch da última atividade"]
            ["rich_text"][0]["text"]["content"],
            "feature/pipeline",
        )


if __name__ == "__main__":
    unittest.main()
