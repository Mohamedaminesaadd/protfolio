"""
GitHub Tools
============

Read-only GitHub tools for the Personal AI Agent.

Architecture:

LangGraph Agent
      ↓
GitHub Tools
      ↓
GitHub REST API
      ↓
Repositories / README / Files

Tools:

1. search_github_repositories()
2. find_my_github_project()
3. get_github_repository()
4. get_github_readme()
5. get_github_file()
"""

import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GITHUB_TOKEN = os.getenv(
    "GITHUB_TOKEN",
    None,
)

GITHUB_OWNER = os.getenv(
    "GITHUB_OWNER",
    "Mohamedaminesaadd",
)

GITHUB_API_URL = "https://api.github.com"


# ============================================================
# HEADERS
# ============================================================

def get_headers() -> dict:
    """
    Build GitHub API request headers.
    """

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = (
            f"Bearer {GITHUB_TOKEN}"
        )

    return headers


# ============================================================
# GENERIC GET REQUEST
# ============================================================

def github_get(endpoint: str):
    """
    Perform a GET request against GitHub REST API.

    Returns:
        dict/list  -> successful response
        None       -> 404 not found

    Raises:
        RuntimeError -> other API errors
    """

    url = f"{GITHUB_API_URL}{endpoint}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=15,
    )

    # --------------------------------------------------------
    # NOT FOUND
    # --------------------------------------------------------

    if response.status_code == 404:
        return None

    # --------------------------------------------------------
    # UNAUTHORIZED
    # --------------------------------------------------------

    if response.status_code == 401:
        raise RuntimeError(
            "GitHub authentication failed. "
            "Check GITHUB_TOKEN."
        )

    # --------------------------------------------------------
    # FORBIDDEN / RATE LIMIT
    # --------------------------------------------------------

    if response.status_code in (403, 429):

        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        raise RuntimeError(
            "GitHub API access was forbidden "
            "or rate limited. "
            f"Remaining requests: {remaining}"
        )

    # --------------------------------------------------------
    # OTHER ERRORS
    # --------------------------------------------------------

    if response.status_code != 200:

        raise RuntimeError(
            f"GitHub API error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return response.json()


# ============================================================
# TOOL 1 — SEARCH GITHUB
# ============================================================

@tool
def search_github_repositories(
    query: str,
) -> str:
    """
    Search GitHub repositories.

    Use this when the user asks about GitHub repositories
    or wants to find a repository.
    """

    encoded_query = requests.utils.quote(
        query
    )

    data = github_get(
        "/search/repositories"
        f"?q={encoded_query}"
        "&per_page=10"
    )

    if not data:

        return (
            "No GitHub repositories were found."
        )

    repositories = data.get(
        "items",
        [],
    )

    if not repositories:

        return (
            "No GitHub repositories were found."
        )

    results = []

    for repo in repositories:

        results.append(
            f"""
Repository:
{repo.get("full_name")}

Name:
{repo.get("name")}

Description:
{repo.get("description")}

URL:
{repo.get("html_url")}

Language:
{repo.get("language")}

Stars:
{repo.get("stargazers_count")}

Forks:
{repo.get("forks_count")}
"""
        )

    return "\n".join(results)


# ============================================================
# TOOL 2 — FIND MY PROJECT
# ============================================================

@tool
def find_my_github_project(
    project_name: str,
) -> str:
    """
    Find Mohamed Amine Saad's GitHub repository
    related to a project.

    Use this tool when the user mentions a project
    but the exact GitHub repository name is unknown.

    IMPORTANT:
    Use this before get_github_repository() when
    the repository name is not known exactly.
    """

    query = (
        f"user:{GITHUB_OWNER} "
        f"{project_name}"
    )

    encoded_query = requests.utils.quote(
        query
    )

    data = github_get(
        "/search/repositories"
        f"?q={encoded_query}"
        "&per_page=10"
    )

    if not data:

        return (
            f'No GitHub repository was found '
            f'for project "{project_name}".'
        )

    repositories = data.get(
        "items",
        [],
    )

    if not repositories:

        return (
            f'No GitHub repository was found '
            f'for project "{project_name}" '
            f'for user "{GITHUB_OWNER}".'
        )

    results = []

    for repo in repositories:

        results.append(
            f"""
Repository:
{repo.get("full_name")}

Name:
{repo.get("name")}

Description:
{repo.get("description")}

URL:
{repo.get("html_url")}

Language:
{repo.get("language")}

Stars:
{repo.get("stargazers_count")}

Forks:
{repo.get("forks_count")}
"""
        )

    return "\n".join(results)


# ============================================================
# TOOL 3 — GET REPOSITORY
# ============================================================

@tool
def get_github_repository(
    owner: str,
    repo: str,
) -> str:
    """
    Get information about a specific GitHub repository.

    IMPORTANT:
    The owner and repository name must be exact.

    Example:

        owner = "Mohamedaminesaadd"
        repo = "project-name"
    """

    data = github_get(
        f"/repos/{owner}/{repo}"
    )

    # --------------------------------------------------------
    # Repository not found
    # --------------------------------------------------------

    if data is None:

        return f"""
Repository not found:

{owner}/{repo}

The repository name may be incorrect.

Use find_my_github_project() first
if the exact repository name is unknown.
"""

    return f"""
Repository:
{data.get("full_name")}

Name:
{data.get("name")}

Description:
{data.get("description")}

URL:
{data.get("html_url")}

Language:
{data.get("language")}

Stars:
{data.get("stargazers_count")}

Forks:
{data.get("forks_count")}

Open issues:
{data.get("open_issues_count")}

Created:
{data.get("created_at")}

Updated:
{data.get("updated_at")}
"""


# ============================================================
# TOOL 4 — GET README
# ============================================================

@tool
def get_github_readme(
    owner: str,
    repo: str,
) -> str:
    """
    Retrieve the README of a GitHub repository.

    Use this when you need to understand what
    a repository/project is about.
    """

    data = github_get(
        f"/repos/{owner}/{repo}/readme"
    )

    if data is None:

        return f"""
README could not be found.

Repository:
{owner}/{repo}
"""

    download_url = data.get(
        "download_url"
    )

    if not download_url:

        return (
            f"README not found for "
            f"{owner}/{repo}."
        )

    response = requests.get(
        download_url,
        headers=get_headers(),
        timeout=15,
    )

    if response.status_code == 404:

        return (
            f"README not found for "
            f"{owner}/{repo}."
        )

    if response.status_code != 200:

        return (
            f"Could not retrieve README. "
            f"Status: {response.status_code}"
        )

    return f"""
Repository:
{owner}/{repo}

README:

{response.text}
"""


# ============================================================
# TOOL 5 — GET FILE
# ============================================================

@tool
def get_github_file(
    owner: str,
    repo: str,
    path: str,
) -> str:
    """
    Read a file from a GitHub repository.

    Example:

        owner = "Mohamedaminesaadd"
        repo = "project-name"
        path = "README.md"
    """

    encoded_path = requests.utils.quote(
        path,
        safe="/",
    )

    data = github_get(
        f"/repos/{owner}/{repo}/contents/{encoded_path}"
    )

    if data is None:

        return f"""
File not found.

Repository:
{owner}/{repo}

Path:
{path}
"""

    # --------------------------------------------------------
    # Directory
    # --------------------------------------------------------

    if isinstance(data, list):

        return f"""
The specified path is a directory.

Repository:
{owner}/{repo}

Path:
{path}

Please provide the path of a specific file.
"""

    # --------------------------------------------------------
    # Download URL
    # --------------------------------------------------------

    download_url = data.get(
        "download_url"
    )

    if not download_url:

        return (
            f"Could not retrieve file "
            f"{path}."
        )

    response = requests.get(
        download_url,
        headers=get_headers(),
        timeout=15,
    )

    if response.status_code == 404:

        return f"""
File not found.

Repository:
{owner}/{repo}

Path:
{path}
"""

    if response.status_code != 200:

        return (
            f"Could not retrieve file. "
            f"Status: {response.status_code}"
        )

    return f"""
Repository:
{owner}/{repo}

File:
{path}

Content:

{response.text}
"""


# ============================================================
# TOOL LIST
# ============================================================

github_tools = [
    search_github_repositories,
    find_my_github_project,
    get_github_repository,
    get_github_readme,
    get_github_file,
]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 80)
    print("GITHUB TOOLS")
    print("=" * 80)

    print("\nGitHub owner:")
    print(GITHUB_OWNER)

    print("\nToken configured:")

    if GITHUB_TOKEN:
        print("YES")
    else:
        print("NO")

    print("\nAvailable tools:")

    for github_tool in github_tools:

        print(
            f"- {github_tool.name}"
        )