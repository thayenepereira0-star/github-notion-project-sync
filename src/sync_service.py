from datetime import datetime, timezone
from typing import Any

from events import extract_issue_references, push_activity


def rich_text_property(value: str) -> dict[str, Any]:
    return {
        "rich_text": [
            {
                "type": "text",
                "text": {"content": value[:2000]},
            }
        ]
    }


def build_notion_properties(
    repository_data: dict[str, Any],
    activity: dict[str, str] | None = None,
) -> dict[str, Any]:
    repo_url = repository_data["html_url"]
    default_branch = repository_data["default_branch"]
    pushed_at = repository_data.get("pushed_at")

    if activity and activity.get("timestamp"):
        pushed_at = activity["timestamp"]

    if not pushed_at:
        pushed_at = datetime.now(timezone.utc).isoformat()

    properties: dict[str, Any] = {
        "Repositório GitHub": {"url": repo_url},
        "Branches relevantes": rich_text_property(default_branch),
        "Issues GitHub": {"url": f"{repo_url}/issues"},
        "Pull requests GitHub": {"url": f"{repo_url}/pulls"},
        "Última atualização GitHub": {
            "date": {"start": pushed_at}
        },
    }

    if activity and activity.get("message"):
        properties["Última atividade"] = rich_text_property(
            activity["message"]
        )
        properties["Branch da última atividade"] = rich_text_property(
            activity.get("branch") or default_branch
        )

    return properties


class SyncService:
    def __init__(
        self,
        github_client,
        notion_client,
        projects_data_source_id: str,
    ) -> None:
        self.github = github_client
        self.notion = notion_client
        self.projects_data_source_id = projects_data_source_id

    def sync(
        self,
        repository: str,
        event_name: str,
        event_payload: dict[str, Any],
    ) -> dict[str, Any]:
        repository_data = self.github.fetch_repository_metadata(
            repository
        )

        notion_page_id = self.notion.find_project_page(
            self.projects_data_source_id,
            repository_data["html_url"],
        )

        activity = None
        if event_name == "push":
            activity = push_activity(event_payload)
        elif event_name == "workflow_dispatch":
            activity = self.github.fetch_latest_commit(
                repository,
                repository_data["default_branch"],
            )

        properties = build_notion_properties(
            repository_data,
            activity,
        )

        self.notion.update_page(
            notion_page_id,
            properties,
        )

        references = []
        if activity:
            references = extract_issue_references(
                activity.get("message")
            )

        return {
            "repository": repository_data["full_name"],
            "notion_page_id": notion_page_id,
            "default_branch": repository_data["default_branch"],
            "activity": activity,
            "issue_references": references,
        }
