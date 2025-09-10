import sqlite3

# Connect to the database (exam.db)
conn = sqlite3.connect('exam.db')
cur = conn.cursor()

# Create a table for demonstration
cur.execute('''CREATE TABLE IF NOT EXISTS demo(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);''')

# Start a transaction explicitly
cur.execute('BEGIN;')  # or conn.execute('BEGIN;')
print("Transaction started.")

# Insert a row
cur.execute('INSERT INTO demo (name) VALUES (?);', ('Alice',))
print("Inserted Alice.")

# Decide to rollback (undo the insert)
conn.rollback()
print("Rolled back. Alice will NOT be in the table.")

# Check table contents after rollback
cur.execute('SELECT * FROM demo;')
print("After rollback:", cur.fetchall())

# Start another transaction
cur.execute('BEGIN;')
print("Transaction started again.")

# Insert a row
cur.execute('INSERT INTO demo (name) VALUES (?);', ('Bob',))
print("Inserted Bob.")

# Commit the transaction (save changes)
conn.commit()
print("Committed. Bob will be in the table.")

# Check table contents after commit
cur.execute('SELECT * FROM demo;')
print("After commit:", cur.fetchall())

# Close connection
conn.close()

# --- Explanation ---
# BEGIN starts a transaction (changes are not permanent yet).
# COMMIT saves all changes made in the transaction.
# ROLLBACK undoes all changes made since the last