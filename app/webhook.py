from fastapi import APIRouter, Request
from app.github_service import get_pr_diff
from app.llm_reviewer import review_code
from app.github_commenter import post_review_comments
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    event = request.headers.get("X-GitHub-Event")
    if event != "pull_request":
        return {"status": "ignored"}

    if payload.get("action") in ["opened", "synchronize", "reopened"]:
        pr_number = payload["pull_request"]["number"]
        repo_name = payload["repository"]["full_name"]
        commit_id = payload["pull_request"]["head"]["sha"]

        try:
            diff = get_pr_diff(repo_name, pr_number)

            review = review_code(diff[:3000])

            print("\n🤖 AI REVIEW:\n", review)

            # ✅ POST TO GITHUB
            if isinstance(review, list):
                post_review_comments(repo_name, pr_number, commit_id, review)

            return {"status": "review posted"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    return {"status": "ok"}