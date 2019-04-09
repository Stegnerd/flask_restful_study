
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

import sqlite3


class Item(Resource):
    # reqparser makes sure to look at the payload and look for
    # certian properties that match certain types
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True,
                        help="this field cannot be left blank!")

    # this means you need to pasgs in a jwt tokenm
    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}
        return {"message": "item not found"}, 404

    # must have the same name and post parameters
    def post(self, name):

        # if this can't attach then it causess an error
        # force=true means you don't have to have contenttype in the header
        # silent=True means that doesn't autoformat but it just returns null
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": "An item already exists with this name, {}".format(name)}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        # look for all items that aren't that one
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            # update is a built in method for dictionary
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"Items": items}
