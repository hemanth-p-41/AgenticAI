import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dev.db'))
print('DB:', db_path)
con = sqlite3.connect(db_path)
cur = con.cursor()
try:
    cur.execute("ALTER TABLE resumes ADD COLUMN file_path VARCHAR(1024)")
    print('Added column file_path')
except Exception as e:
    print('Error:', e)
con.commit()
con.close()
