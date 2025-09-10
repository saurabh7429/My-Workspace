import sqlite3

src = sqlite3.connect('source.db')
dst = sqlite3.connect('destination.db')

src.execute('''CREATE TABLE IF NOT EXISTS demo(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);''')

rows = [('Alice',), ('saurabh',), ('rahul',), ('rohit',), ('ankit',)]
src.executemany('INSERT INTO demo (name) VALUES (?);', rows)
src.commit()

# with dst:
#     src.backup(dst)
src.backup(dst)
cur = dst.cursor()

cur.execute('select * from demo;')
for a in cur.fetchall():
    print(a)


