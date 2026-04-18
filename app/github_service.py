from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

def get_pr_diff(repo_name, pr_number):
    token = os.getenv("GITHUB_TOKEN")

    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    diff = ""

    for file in pr.get_files():
        diff += f"\n--- {file.filename} ---\n"
        diff += file.patch or ""

    return diff