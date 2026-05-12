import sqlite3


def save_review(
    developer,
    repo_name,
    pr_number,
    severity,
    comment,
    file_path,
    line_number
):

    conn = sqlite3.connect("reviews.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reviews (
        developer,
        repo_name,
        pr_number,
        severity,
        comment,
        file_path,
        line_number
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        developer,
        repo_name,
        pr_number,
        severity,
        comment,
        file_path,
        line_number
    ))

    conn.commit()
    conn.close()

    print("✅ Review saved to database")