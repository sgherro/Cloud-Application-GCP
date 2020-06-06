from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from music import MusicCatalog
from urllib.parse import quote
from marshmallow import Schema, fields, ValidationError, validate
from uuid import UUID

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

mc = MusicCatalog()

def uuid_validation(uuid_test, version = 4):
    try:
        uuid = UUID(uuid_test, version=version)
    except ValueError:
        return False
    return str(uuid)== uuid_test

class ArtistSchema(Schema):
    name = fields.Str(required=True)


def validate_artist(json):
    try:
        ret = ArtistSchema().load(json)
        return ret
    except ValidationError as err:
        print(err.messages)
        return None

class DiscSchema(Schema):
    name = fields.Str(required=True)
    year = fields.Int(validate=validate.Range(min=1990, max=2020))
    genre = fields.Str(validate=validate.OneOf(['rock', 'pop', 'electronic','dance']))


def validate_disc(json):
    try:
        ret = DiscSchema().load(json)
        return ret
    except ValidationError as err:
        print(err.messages)
        return None

class InsertArtist(Resource):
    def post(self, artist_id):
        if artist_id is None:
            print("ID ERROR")
            return None, 409

        if not uuid_validation(artist_id):
            print("UID ERROR")
            return None, 409

        try:
            ref = request.get_json()
            if not validate_artist(ref):
                print("ERROR ARTIST")
                return None, 409
            artist_name = ref['name']
            artist = mc.get_artist(artist_id)
            if artist is None:
                mc.post_artist(artist_id, artist_name)
            else:
                print("ERROR ARTISTS ALREADY EXIST")
                return None, 409
        except Exception:
            print("ERROR JSON")
            return None, 409
        return None, 201

    def get(self, artist_id):
        if artist_id is None:
            return None, 404
        if not uuid_validation(artist_id):
            return None, 404
        
        try:
            artist = mc.get_artist(artist_id)
            return artist, 200
        except Exception:
            return None, 404

class InsertDisc(Resource):
    def post(self, artist_id, disc_id):
        if not uuid_validation(disc_id):
            print("UUID FAILED")
            return None, 400
        if not uuid_validation(artist_id):
            return None, 409
        
        ref = request.get_json()
        if not validate_disc(ref):
            print("ERROR DISC VALIDATION")
            return None, 400
        if mc.get_disc(disc_id,artist_id):
            return None, 400

        if not mc.post_disc(disc_id,artist_id,ref['name'],ref['year'],ref['genre']):
            return None, 400
        return None, 201
    
    def get(self, artist_id, disc_id):
        if not uuid_validation(artist_id) or not uuid_validation(disc_id):
            return None, 400

        try:
            ref = mc.get_disc(disc_id, artist_id)
            if ref is not None:
                return ref, 200
            else:
                return None, 400
        except Exception:
            return None , 400
        
class SearchGenre(Resource):
    def get(self, genre):
        if genre not in ['pop', 'rock','electronic','dance']:
            print("GENRE IS WRONG")
            return None, 403
        try:
            ref = mc.get_genre(genre)
            print(ref)
            return ref, 200
        except Exception:
            return None, 400


api.add_resource(InsertArtist, f'{basePath}/artist/<string:artist_id>')
api.add_resource(InsertDisc, f'{basePath}/disc/<string:artist_id>/<string:disc_id>')
api.add_resource(SearchGenre, f'{basePath}/genre/<string:genre>')


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)