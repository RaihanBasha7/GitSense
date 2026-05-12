from github import Github
import os
from dotenv import load_dotenv

token = os.getenv("GITHUB_TOKEN")
g = Github(token)

load_dotenv()
def get_pr_diff(repo_name, pr_number):

    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    full_diff = ""

    for file in pr.get_files():

        full_diff += f"\n\nFile: {file.filename}\n"

        if file.patch:
            full_diff += file.patch

    return full_diff