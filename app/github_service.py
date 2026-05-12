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
    valid_lines = {}

    for file in pr.get_files():

        full_diff += f"\n\nFile: {file.filename}\n"

        if file.patch:

            full_diff += file.patch

            # Store changed lines
            valid_lines[file.filename] = []

            patch_lines = file.patch.split("\n")

            current_line = 0

            for line in patch_lines:

                # Detect diff hunk
                if line.startswith("@@"):

                    parts = line.split(" ")

                    new_file_info = parts[2]

                    current_line = int(
                        new_file_info.split(",")[0].replace("+", "")
                    )

                elif line.startswith("+") and not line.startswith("+++"):

                    valid_lines[file.filename].append(current_line)

                    current_line += 1

                elif not line.startswith("-"):

                    current_line += 1

    return full_diff, valid_lines