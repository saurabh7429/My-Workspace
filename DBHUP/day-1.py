#importing module
import sqlite3
from tabulate import tabulate

#connecting to database
conn = sqlite3.connect('day-1.db')
print("database created")

#creating cursor object
cursor = conn.cursor()

#create table
cursor.execute('''CREATE TABLE IF NOT EXISTS EMPLOYEE(ID INTEGER PRIMARY KEY, NAME TEXT NOT NULL, AGE INTEGER,SALARY REAL);''')
print("Table  CREATED")

# Clear table before inserting (optional)
cursor.execute("DELETE FROM EMPLOYEE")

#INSERT VALUES
conn.execute('''insert into employee ('name', age, salary) values ('Saurav', 18, 2000)''')
conn.execute('''insert into employee ('name', age, salary) values ('Ayush', 17, 1000)''')
conn.execute('''insert into employee ('name', age, salary) values ('ganpat', 20, 2000)''')
conn.execute('''insert into employee ('name', age, salary) values ('RIShab', 23, 3000)''')
conn.execute('''insert into employee ('name', age, salary) values ('Raj', 18, 5000)''')
conn.commit()



# print table and data
cursor.execute('''select * from employee;''')
rows = cursor.fetchall()
headers = [desc[0] for desc in cursor.description]
print(tabulate(rows, headers, tablefmt="fancy_grid"))

cursor.execute('''UPDATE employee SET age = ? WHERE name = ?''', (28, "Raj"))
print("Updated rows:", cursor.rowcount)

cursor.execute('''select * from employee;''')
rows = cursor.fetchall()
headers = [desc[0] for desc in cursor.description]
print(tabulate(rows, headers, tablefmt="fancy_grid"))