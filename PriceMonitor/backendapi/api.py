from flask import Flask
from flask_restful import Resource, Api, request
from datetime import datetime
from marshmallow import Schema, fields, validate
from uuid import UUID
from price import *

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'e3esacosdncwefn3rif3ufcs'

basePath = '/api/v1' 
price = Price()

def uuid_validation(uuid_test, version = 4):
    try:
        uuid = UUID(uuid_test, version=version)
    except ValueError:
        return False
    return str(uuid)== uuid_test

class ItemSchema(Schema):
    percentage = fields.Integer(required=True, validate= validate.Range(min=1, max=100))

def validate_item(json):
    try:
        ret = ItemSchema().load(json)
        return ret
    except ValidationError as err:
        print(err.messages)
        return None

class MonitorObject(Resource):

    def post(self, user, object_uri):
            if not uuid_validation(user):
               print("UUID NOT VALID")
               return None, 400
            ref = request.get_json()
            if not validate_item(ref):
                print("JSON NOT VALID")
                return None, 400
            req = price.get_object(user, object_uri)
            if not req:
                price.post_object(user,object_uri, ref['percentage'])
                return None, 201
            else:
                return None, 409
            return None, 400

    def get(self, user, object_uri):
        if not uuid_validation(user) or not object_uri:
            return None, 404
        ref = price.get_object(user, object_uri)
        if ref:
            return ref, 200
        return None, 404

class Details(Resource):

    def get(self, object_uri):
        if not object_uri:
            print("URI NOT VALID")
            return None, 404
        print(object_uri)
        ref = price.get_details(object_uri)
        print(ref)
        if ref:
            return ref, 200
        return None, 404

class DetailsUser(Resource):

    def get(self, user):
        if not uuid_validation(user):
            return None, 404
        ref = price.get_list(user)
        if ref:
            return ref, 200
        return None, 400

api.add_resource(MonitorObject, f'{basePath}/monitor/<string:user>/<string:object_uri>')
api.add_resource(Details, f'{basePath}/details/<string:object_uri>')
api.add_resource(DetailsUser, f'{basePath}/list/<string:user>')

if __name__=='__main__':
    app.run(host='127.0.0.1', debug = True)