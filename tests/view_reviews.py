import sqlite3

conn = sqlite3.connect("reviews.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM reviews")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
