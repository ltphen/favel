import sqlite3
import time
db = sqlite3.connect(".cache")
cursor = db.execute('''SELECT name FROM sqlite_schema 
WHERE type IN ('table','view') 
AND name NOT LIKE 'sqlite_%'
ORDER BY 1;''')
for row in cursor:
    print(row)
