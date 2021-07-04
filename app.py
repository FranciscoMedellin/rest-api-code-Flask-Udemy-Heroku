from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from resources.item import Item,ItemList

from security import authenticate, identity
from resources.user import UserRegister

from db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'jose'
api = Api(app)

#app.config['JWT_AUTH_URLRULE'] = '/login' # if you want change default /auth path 
jwt = JWT(app, authenticate, identity) # creates a end point ( /auth ), when i call to a post it call t authenticate method and when we call a get that required identity call identity

#items = []

api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)

