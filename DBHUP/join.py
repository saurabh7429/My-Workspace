import sqlite3

# Connect to join.db (will create if not exists)
conn = sqlite3.connect('join.db')
cur = conn.cursor()

# Create Students table
cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# Create Courses table
cur.execute('''
CREATE TABLE IF NOT EXISTS courses (
    student_id INTEGER,
    course TEXT NOT NULL
)
''')

# Clear tables for fresh run
cur.execute('DELETE FROM students;')
cur.execute('DELETE FROM courses;')
conn.commit()

# Insert 5 records in students
students_data = [
    (1, 'Aman'),
    (2, 'Bina'),
    (3, 'Chirag'),
    (4, 'Deepak'),
    (7, 'Esha')
]
cur.executemany('INSERT INTO students (id, name) VALUES (?, ?);', students_data)

# Insert 5 records in courses (3 matching student_id, 2 non-matching)
courses_data = [
    (1, 'Python'),    # matches Aman
    (2, 'DBMS'),      # matches Bina
    (3, 'C++'),       # matches Chirag
    (6, 'Java'),      # not matching
    (7, 'SQL')        # not matching
]
cur.executemany('INSERT INTO courses (student_id, course) VALUES (?, ?);', courses_data)
conn.commit()

# Show all students
print("Students table:")
for row in cur.execute('SELECT * FROM students;'):
    print(row)

# Show all courses
print("\nCourses table:")
for row in cur.execute('SELECT * FROM courses;'):
    print(row)

