from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "9cd1bb56-567f-11e9-8647-d663bd873d93"
api = Api(app)

# creates endpoint /auth
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# this way we only run this if we called app.py not if we import something from this
if __name__ == "__main__":
    app.run(port=5000, debug=True)
