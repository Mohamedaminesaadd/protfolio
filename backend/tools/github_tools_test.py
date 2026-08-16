
from backend.tools.github_tool import (
    search_github_repositories,
    get_github_repository,
    get_github_readme,
    get_github_file,
)


# ============================================================
# CONFIGURATION
# ============================================================

GITHUB_OWNER = "Mohamedaminesaadd"


# ============================================================
# TEST 1 — SEARCH
# ============================================================

def test_search():

    print("\n")
    print("=" * 80)
    print("TEST 1 — SEARCH REPOSITORIES")
    print("=" * 80)

    result = search_github_repositories.invoke(
        {
            "query": "Mohamedaminesaadd ECG"
        }
    )

    print(result)


# ============================================================
# TEST 2 — REPOSITORY
# ============================================================

def test_repository():

    print("\n")
    print("=" * 80)
    print("TEST 2 — GET REPOSITORY")
    print("=" * 80)

    result = get_github_repository.invoke(
        {
            "owner": GITHUB_OWNER,
            "repo": "Big-Data-Twitter-Analysis-System-using-Hadoop",
        }
    )

    print(result)


# ============================================================
# TEST 3 — README
# ============================================================

def test_readme():

    print("\n")
    print("=" * 80)
    print("TEST 3 — GET README")
    print("=" * 80)

    result = get_github_readme.invoke(
        {
            "owner": GITHUB_OWNER,
            "repo": "Big-Data-Twitter-Analysis-System-using-Hadoop",
        }
    )

    print(result)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    test_search()

    test_repository()

    test_readme()
