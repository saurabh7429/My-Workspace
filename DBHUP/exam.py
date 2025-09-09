import sqlite3
conn = sqlite3.connect('exam.db')
cur = conn.cursor()

cur.execute('''create table if not exists student(id integer primary key,name text,age integer);''')
print("db created")


data = [
    ('saurav',19),
    ('aus',25),
    ('ganpat',22)
]
# delete
cur.execute('''delete from student;''')

#insert
cur.executemany('''insert into student ('name',age) values (?,?)''',data)
conn.commit()

print("\n\n after update ")
cur.execute('''select * from student;''')
for a in cur.fetchall():
    print(a)
#update 
cur.execute('''update student set age = ? where id = ?;''',(20,2))


#access
print("\n\n after update ")
cur.execute('''select * from student;''')
for a in cur.fetchall():
    print(a)




