import sqlite3
DATABASE = 'hw13.db'
conn = sqlite3.connect(DATABASE)

c = conn.cursor()

c.execute('''insert into STUDENTS (FIRSTNAME, LASTNAME) values ('f','l')''')
conn.commit()

c.execute('''select * from STUDENTS''')
print c.fetchall()