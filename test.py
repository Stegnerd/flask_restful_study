import sqlite3

connection = sqlite3.connect("data.db")

# responsible for queries and storing result
cursor = connection.cursor()

# create a table in db
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)


user = (1, "dalton", 'cats')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)

users = [
    (2, "darrien", 'dog'),
    (3, "marybeth", 'bird'),
    (4, "aidan", 'fish')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
