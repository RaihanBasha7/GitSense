import sqlite3

def get_pending_reviews(repo_name, pr_number):

    conn = sqlite3.connect("reviews.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, comment, file_path, line_number
    FROM reviews
    WHERE repo_name = ?
    AND pr_number = ?
    AND status = 'pending'
    """, (repo_name, pr_number))

    rows = cursor.fetchall()

    conn.close()

    return rows

def update_review_status(review_id, status):

    conn = sqlite3.connect("reviews.db")

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE reviews
    SET status = ?
    WHERE id = ?
    """, (status, review_id))

    conn.commit()
    conn.close()

    print(f"✅ Review {review_id} marked as {status}")

def detect_fixed_reviews(repo_name, pr_number, latest_diff):

    pending_reviews = get_pending_reviews(
        repo_name,
        pr_number
    )

    for review in pending_reviews:

        review_id = review[0]
        comment = review[1]

        # VERY SIMPLE heuristic for now
        if "snake_case" in comment.lower():

            if "GetUserName" not in latest_diff:

                update_review_status(
                    review_id,
                    "accepted"
                )

        elif "docstring" in comment.lower():

            if '"""' in latest_diff:

                update_review_status(
                    review_id,
                    "accepted"
                )

        elif "try-except" in comment.lower():

            if "try:" in latest_diff:

                update_review_status(
                    review_id,
                    "accepted"
                )