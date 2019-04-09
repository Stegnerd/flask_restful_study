import sqlite3


class User:
    # _id becuase id is a reserved keyword
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    # added this since self wasn't used and we called User instantiation
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # execute has to be in the form of a tuple
        result = cursor.execute(query, (username,))
        # gets the first result in the set , and if empty returns None
        row = result.fetchone()
        if row:
            # this expands into row[0],row[1],row[2]
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"

        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
