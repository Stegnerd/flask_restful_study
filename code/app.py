from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key = "9cd1bb56-567f-11e9-8647-d663bd873d93"
api = Api(app)

# creates endpoint /auth
jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    # reqparser makes sure to look at the payload and look for
    # certian properties that match certain types
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True,
                        help="this field cannot be left blank!")

    # this means you need to pasgs in a jwt tokenm
    @jwt_required()
    def get(self, name):
        # this gives us the first item found by filter
        item = next(filter(lambda x: x["name"] == name, items), None)
        # can also type 200 if item else 404
        return {"item": item}, 200 if item is not None else 404

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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
