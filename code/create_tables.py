import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# when we want auto index we have to use INTEGER instead of int
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# real = decimal
create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

cursor.execute("INSERT INTO items VALUES ('test',10.99)")

connection.commit()

connection.close()
