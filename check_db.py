
from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)
tables = cursor.fetchall()

print("Tables found:", tables)

for (table_name,) in tables:
    print(f"\n--- {table_name} ---")
    cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 10')
    print(cursor.fetchall())

conn.close()
