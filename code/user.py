from flask_restful import Resource, reqparse
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


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str,
                        required=True, help="This field is required")
    parser.add_argument("password", type=str,
                        required=True, help="This field is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message": "A user with tha name already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # pass in null since table index is auto increment
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created succesfully."}, 201
