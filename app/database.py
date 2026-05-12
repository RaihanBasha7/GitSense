import sqlite3

# Create connection
conn = sqlite3.connect("reviews.db")

# Create cursor
cursor = conn.cursor()

# Create reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    developer TEXT,
    repo_name TEXT,
    pr_number INTEGER,
    severity TEXT,
    comment TEXT,
    file_path TEXT,
    line_number INTEGER,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("✅ Reviews database initialized")