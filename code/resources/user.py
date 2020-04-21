import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# Resource so we can add it to Flask RESTful and create endpoints
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Cannot leave username blank!")
    parser.add_argument('password',
        type=str,
        required=True,
        help="Cannot leave password blank!")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"A user with username '{data['username']}' already exists."}, 400

        # ** unpacks the dictionary to data['username'], data['password']
        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User created successfully."}, 201
