from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# Don't need to use jsonify with Flask RESTful
class Item(Resource):
    # using parser so that if someone sends a request with a different name, it
    # should not change the name. It should only change the price.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = self.parser.parse_args()
        # not request.getJson() if you use the parser

        # ** unpacks data to data['price'], data['store_id']
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': f"Item '{name}' deleted."}

    def put(self, name):
        data = self.parser.parse_args()
        # not request.getJson() if you use the parser

        item = ItemModel.find_by_name(name)

        if item is None:
            # ** unpacks data to data['price'], data['store_id']
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
