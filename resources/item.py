import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

#import sys
#sys.path.append('C:/Users/52866/Documents/APRENDIZAJE/Curso REST APIs with Flask and Python/rest-api-sections-master/section6code/models') #folder which contains model, snn etc.,
#from models.item import ItemModel

class Item(Resource): #/item/<name>
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This file cannot be left blank"
        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'meesage':'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400 #bad request code

        data = Item.parser.parse_args()
        
        item = ItemModel(name , data['price'])

        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred inserting the item"}, 500 #internal server error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item == None: 
           item = ItemModel(name, data['price']) # if doesnt exists create a new object
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        try:
            result = cursor.execute(query)
        except:
            return {'message':'An error occurred reading data base'}
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})

        connection.close()

        return {'items': items}
