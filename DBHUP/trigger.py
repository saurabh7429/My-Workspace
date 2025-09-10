import sqlite3

# Step 1: Database create / connect
# Agar file exist nahi karti toh 'students.db' ek new file ke sath DB ban jayega
conn = sqlite3.connect("students.db")
cur = conn.cursor()

# Step 2: Main table banani (students)
# Yaha ek students table banayi jisme id, name aur marks store honge
cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- har student ka unique ID
    name TEXT NOT NULL,                   -- student ka naam
    marks INTEGER                         -- student ke marks
)
''')

# Step 3: Audit table banani (log ke liye)
# Jab bhi koi INSERT hoga students me, toh trigger is audit table me log save karega
cur.execute('''
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,         -- yaha action ka detail aayega (Inserted / Updated etc.)
    ts TEXT              -- timestamp kab action hua
)
''')

# Step 4: Trigger banana
# AFTER INSERT trigger students table pe ban raha hai
# Matlab: students me koi naya student insert hote hi trigger chalega
cur.execute('''
CREATE TRIGGER IF NOT EXISTS log_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
   -- "NEW" keyword ka matlab hai naya inserted row
   -- Yaha ek record audit table me add ho jayega
   INSERT INTO audit(action, ts) 
   VALUES ('Inserted student: ' || NEW.name, datetime('now'));
END;
''')

# Step 5: Data insert karna students table me
# Jab hum INSERT karenge students table me, toh trigger automatically fire hoga
cur.execute("INSERT INTO students (name, marks) VALUES (?, ?)", ("Aman", 85))
cur.execute("INSERT INTO students (name, marks) VALUES (?, ?)", ("Bina", 92))
conn.commit()

# Step 6: Audit table ka data dekhna
# Trigger ne kya kiya uska result audit table me check karte hain
cur.execute("SELECT * FROM audit")
rows = cur.fetchall()

print("Audit Log:")
for row in rows:
    print(row)  # (id, action, timestamp)

# Step 7: Example of DROP TRIGGER
# Agar trigger delete karna ho toh:
# cur.execute("DROP TRIGGER IF EXISTS log_insert")

conn.close()
