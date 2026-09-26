"""One-off fix: update the demo account password hashes in ibsu_lunch.db
to match the corrected admin123 / student123 credentials.

Run from the project root:
    python fix_hashes.py
"""
import sqlite3

ADMIN_HASH = "pbkdf2_sha256$310000$2f9d24fa2b95a074a29cd742cf1ee593$10c24a4c1fa83b2ad20a7f3c09ad1e93dc4ab4cb97bce15b807fcd746657873d"
STUDENT_HASH = "pbkdf2_sha256$310000$b7c989819186db6879f9f6cf20196693$c0f3671224e56327d17ed0e215a09e8336ce291598341c5a30c2dd46adb1fa09"

conn = sqlite3.connect("database/ibsu_lunch.db")
conn.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (ADMIN_HASH,))
conn.execute("UPDATE users SET password_hash = ? WHERE username = 'student'", (STUDENT_HASH,))
conn.commit()

print("Updated. Current rows:")
conn.row_factory = sqlite3.Row
for row in conn.execute("SELECT username, password_hash FROM users"):
    print(dict(row))

conn.close()