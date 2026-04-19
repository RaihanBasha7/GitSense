from github import Github
import os

g = Github(os.getenv("GITHUB_TOKEN"))

def post_review_comments(repo_name, pr_number, comments):
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    for c in comments:
        try:
            pr.create_issue_comment(
                f"[{c['severity'].upper()}] {c['comment']}"
            )
        except Exception as e:
            print(f"❌ Failed to post comment: {e}")