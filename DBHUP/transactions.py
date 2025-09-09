import sqlite3
conn = sqlite3.connect('exam.db')

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS emp(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);''')

cur.execute('''DELETE FROM emp;''')
data = [('saurabh',), ('raj',), ('ganpat',), ('rishab',), ('ayush',)]

cur.executemany('''INSERT INTO emp (name) VALUES (?);''', data)
conn.commit()

cur.execute('''SELECT * FROM emp;''')
for a in cur.fetchall():
    print(a)

print("-------A new data added--------\n\n")
cur.execute('''INSERT INTO emp (name) VALUES ('neha')''')

i = int(input("Data inserted.\nEnter 1 to commit else rollback: "))
if i == 1:
    conn.commit()
else:
    conn.rollback()

cur.execute('''SELECT * FROM emp;''')
for a in cur.fetchall():
    print(a)

cur.close()
conn.close()