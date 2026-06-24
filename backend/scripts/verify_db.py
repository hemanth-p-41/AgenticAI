import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'dev.db')
db_path = os.path.abspath(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

print('DB path:', db_path)
print('\nTables:')
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print('-', row[0])

print('\nSchema details:')
for row in cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table';"):
    print('\nTable:', row[0])
    print(row[1])

print('\nForeign keys:')
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    t = row[0]
    try:
        fks = list(cur.execute(f"PRAGMA foreign_key_list('{t}')"))
        if fks:
            print('\n', t)
            for fk in fks:
                print(' ', fk)
    except sqlite3.DatabaseError:
        pass

conn.close()
