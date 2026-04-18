from fastapi import APIRouter, Request
from app.github_service import get_pr_diff

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    print("📩 Webhook received!")

    if payload.get("action") == "opened":
        pr_number = payload["pull_request"]["number"]
        repo_name = payload["repository"]["full_name"]

        print(f"🔥 PR Opened: #{pr_number}")
        print(f"📦 Repo: {repo_name}")

        diff = get_pr_diff(repo_name, pr_number)

        print("\n📄 DIFF:\n")
        print(diff)

    return {"status": "ok"}