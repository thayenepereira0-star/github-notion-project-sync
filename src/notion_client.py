from typing import Any
import requests

NOTION_API_URL = "https://api.notion.com/v1/pages/{page_id}"
NOTION_DATA_SOURCE_QUERY_URL = (
    "https://api.notion.com/v1/data_sources/{data_source_id}/query"
)
NOTION_VERSION = "2026-03-11"


class NotionClient:
    def __init__(self, token: str) -> None:
        self._token = token

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def find_project_page(
        self,
        data_source_id: str,
        repository_url: str,
    ) -> str:
        response = requests.post(
            NOTION_DATA_SOURCE_QUERY_URL.format(
                data_source_id=data_source_id
            ),
            headers=self.headers,
            json={
                "filter": {
                    "and": [
                        {
                            "property": "Repositório GitHub",
                            "url": {"equals": repository_url},
                        },
                        {
                            "property": "Automação ativa",
                            "checkbox": {"equals": True},
                        },
                    ]
                },
                "page_size": 2,
            },
            timeout=30,
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            raise RuntimeError(
                "No active Notion project matches repository "
                f"{repository_url}."
            )

        if len(results) > 1:
            raise RuntimeError(
                "More than one active Notion project uses the same "
                "repository."
            )

        return results[0]["id"]

    def update_page(
        self,
        page_id: str,
        properties: dict[str, Any],
    ) -> None:
        response = requests.patch(
            NOTION_API_URL.format(page_id=page_id),
            headers=self.headers,
            json={"properties": properties},
            timeout=30,
        )
        response.raise_for_status()
