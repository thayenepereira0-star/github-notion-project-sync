import sys

from config import Settings
from events import read_event_payload
from github_client import GitHubClient
from notion_client import NotionClient
from sync_service import SyncService


def main() -> int:
    try:
        settings = Settings.from_env()

        service = SyncService(
            github_client=GitHubClient(settings.github_token),
            notion_client=NotionClient(settings.notion_token),
            projects_data_source_id=(
                settings.notion_projects_data_source_id
            ),
        )

        result = service.sync(
            repository=settings.repository,
            event_name=settings.event_name,
            event_payload=read_event_payload(settings.event_path),
        )

        print("GitHub → Notion sync completed.")
        print(f"Repository: {result['repository']}")
        print(f"Notion project: {result['notion_page_id']}")
        print(f"Default branch: {result['default_branch']}")

        activity = result.get("activity")
        if activity:
            print(f"Last activity: {activity['message']}")
            print(
                "Activity branch: "
                f"{activity.get('branch') or '-'}"
            )

        references = result.get("issue_references", [])
        if references:
            formatted = ", ".join(
                f"#{number}" for number in references
            )
            print(
                "Issue references detected for future integration: "
                f"{formatted}"
            )

        return 0

    except Exception as exc:
        print(f"Sync error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
