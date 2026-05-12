from github import Github
import os

g = Github(os.getenv("GITHUB_TOKEN"))


def post_review_comments(repo_name, pr_number, commit_id, comments):

    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    commit_id = pr.head.sha

    for c in comments:

        try:

            comment_body = f"[{c['severity'].upper()}] {c['comment']}"

            line = c.get("line")

            # --------------------------------
            # Case 1 → Inline PR Comment
            # Format: "file.py:15"
            # --------------------------------
            if isinstance(line, str) and ":" in line:

                file_path, line_no = line.split(":")
                line_no = int(line_no)

                pr.create_review_comment(
                    body=comment_body,
                    commit=commit_id,
                    path=file_path,
                    line=line_no
                )

                print("✅ Inline comment posted")

            # --------------------------------
            # Case 2 → General PR Comment
            # --------------------------------
            else:

                pr.create_issue_comment(comment_body)

                print("📝 General comment posted")

        except Exception as e:

            print(f"❌ Failed to post comment: {e}")