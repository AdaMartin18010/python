# tech_radar_system/src/collector.py

import os
import requests
from ghapi.all import GhApi

def get_github_data(repo_owner, repo_name):
    """
    Fetches basic repository data from GitHub.
    """
    # 建议将GITHUB_TOKEN设置为环境变量以提高安全性
    api = GhApi(token=os.getenv("GITHUB_TOKEN"))
    try:
        repo = api.repos.get(owner=repo_owner, repo=repo_name)
        return {
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "watchers": repo.watchers_count,
            "last_updated": repo.updated_at,
        }
    except Exception as e:
        print(f"Error fetching data for {repo_owner}/{repo_name}: {e}")
        return None

def get_pypi_data(package_name):
    """
    Fetches basic package data from PyPI.
    """
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        data = response.json()
        return {
            "version": data["info"]["version"],
            "author": data["info"]["author"],
            "summary": data["info"]["summary"],
        }
    except requests.RequestException as e:
        print(f"Error fetching data for {package_name} from PyPI: {e}")
        return None 