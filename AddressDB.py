import sqlite3
connection = sqlite3.connect("addressbook.db")
print("Database opened successfully")
cursor = connection.cursor()
#delete
# cursor.execute('''DROP TABLE Address;''')
# connection.execute("create table Address (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, address TEXT NOT NULL, mobile NUMBER NOT NULL)")
# print("Table created successfully")
# connection.execute("ALTER TABLE Address ADD COLUMN city TEXT")
# connection.execute("ALTER TABLE Address ADD COLUMN pincode NUMBER")
# connection.execute("ALTER TABLE Address ADD COLUMN image TEXT")
# print("table modified successfully")
connection.close()
