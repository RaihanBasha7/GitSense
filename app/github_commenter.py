from github import Github
import os

g = Github(os.getenv("GITHUB_TOKEN"))

def post_review_comments(repo_name, pr_number, commit_id, comments):
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    commit_id = pr.head.sha  # 🔥 VERY IMPORTANT

    for c in comments:
        try:
            # If line info exists → inline comment
            if c.get("line") and ":" in c["line"]:
                file_path, line_no = c["line"].split(":")
                line_no = int(line_no)

                pr.create_review_comment(
                    body=f"[{c['severity'].upper()}] {c['comment']}",
                    commit=commit_id,
                    path=file_path,
                    line=line_no
                )
                print("✅ Inline comment posted")

            else:
                # fallback → normal comment
                pr.create_issue_comment(
                    f"[{c['severity'].upper()}] {c['comment']}"
                )
                print("📝 General comment posted")

        except Exception as e:
            print(f"❌ Failed to post comment: {e}")