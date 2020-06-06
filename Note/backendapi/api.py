from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from uuid import UUID
from marshmallow import fields, validate, ValidationError, Schema
from note import *
import requests

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

note = Note()

def uuid_validation(uuid_test, version = 4):
    try:
        uuid = UUID(uuid_test, version=version)
    except ValueError:
        return False
    return str(uuid)== uuid_test

class ItemSchema(Schema):
    content = fields.Str(required=True,validate=validate.Length(min=1, max=250))

def validate_item(json):
    try:
        ret = ItemSchema().load(json)
        return ret
    except ValidationError as err:
        print(err.messages)
        return None

class InsertNote(Resource):
    def get(self, owner_id, note_id):
        if len(note_id) <5 or len(note_id) >16:
            print("INVALID NOTE ID")
            return None, 400
        try:
            ref = note.get_note(owner_id, note_id)
            if ref:
                return ref, 200
            else:
                return None, 409
        except Exception:
            return None, 409

    def post(self, owner_id, note_id):
        if len(note_id) <5 or len(note_id) >16:
            print("INVALID NOTE ID")
            return None, 400

        if not uuid_validation(owner_id):
            print("INVALID OWNER ID")
            return None, 409
        try:
            ref = request.get_data(as_text=True) #contenuto della nota
            if not ref and not validate_item(ref):
                print("INVALID INPUT DATA")
                return None , 409
            note.post_note(owner_id, note_id, str(ref))
            return None, 201
        except Exception:
            print("ERROR")
            return None, 400    
        
class ShareNote(Resource):
    def post(self, owner_id, recipient_id):
        if not uuid_validation(owner_id) or not uuid_validation(recipient_id):
            print("UUID VALUE NOT VALID")
            return None, 404
        if owner_id == recipient_id:
            print("UUID ARE EQUAL")
            return None, 404
        if not note.check_note(recipient_id):
            print("NO PREVIOUS NOTE")
            return None, 400
        try:
            ref = str(request.get_data(as_text=True))
            if not ref:
                return None, 400
            if len(ref) > 5 or len(ref)<16:
                note.share_note(owner_id, recipient_id, ref)
                return None, 200
            return None, 400
        except Exception:
            return None, 400
        
class StaticAddress(Resource):
    def get(self, note_id):
        if len(note_id) < 5 or len(note_id)>16:
            print("INVALID NOTE ID")
            return None, 409
        ow, n = note.get_address(note_id)
        if n and ow:
            r = requests.get(f"https://api-dot-note-sac1203.appspot.com/api/v1/notes/{ow}/{n}")
            return r.url, 200
        return None, 400
        
api.add_resource(InsertNote, f'{basePath}/notes/<string:owner_id>/<string:note_id>')
api.add_resource(ShareNote, f'{basePath}/share/<string:owner_id>/<string:recipient_id>')
api.add_resource(StaticAddress, f'{basePath}/address/<string:note_id>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)