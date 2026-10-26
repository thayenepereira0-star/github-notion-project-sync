from typing import Any
import requests

GITHUB_API_URL = "https://api.github.com/repos/{repository}"


class GitHubClient:
    def __init__(self, token: str) -> None:
        self._token = token

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def fetch_repository_metadata(self, repository: str) -> dict[str, Any]:
        response = requests.get(
            GITHUB_API_URL.format(repository=repository),
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def fetch_latest_commit(
        self, repository: str, branch: str
    ) -> dict[str, str] | None:
        response = requests.get(
            f"{GITHUB_API_URL.format(repository=repository)}/commits",
            headers=self.headers,
            params={"sha": branch, "per_page": 1},
            timeout=30,
        )
        response.raise_for_status()

        commits = response.json()
        if not commits:
            return None

        latest = commits[0]
        commit_data = latest.get("commit", {})
        author_data = commit_data.get("author", {})
        message = (commit_data.get("message") or "").strip().splitlines()[0]

        return {
            "message": message[:2000],
            "branch": branch,
            "timestamp": author_data.get("date") or "",
            "sha": latest.get("sha") or "",
        }
