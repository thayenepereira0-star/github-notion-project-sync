from dataclasses import dataclass
import os


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    notion_token: str
    notion_projects_data_source_id: str
    github_token: str
    repository: str
    event_name: str
    event_path: str | None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            notion_token=require_env("NOTION_TOKEN"),
            notion_projects_data_source_id=require_env(
                "NOTION_PROJECTS_DATA_SOURCE_ID"
            ),
            github_token=require_env("GH_TOKEN"),
            repository=require_env("GITHUB_REPOSITORY"),
            event_name=os.getenv("GITHUB_EVENT_NAME", "workflow_dispatch"),
            event_path=os.getenv("GITHUB_EVENT_PATH") or None,
        )
