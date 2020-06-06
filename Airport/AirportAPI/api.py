from flask import Flask
from flask_restful import Resource, Api, reqparse
from airports import Airports

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'e3esacosdncwefn3rif3ufcs'

basePath = '/api/v1' #uguale a quello nel file .yaml
airports_util = Airports()

class AirportNames(Resource):
    def get(self, iataCode):
        if len(iataCode) != 3:
            return None, 400
        return_val = airports_util.get_airport_by_iata(iataCode)
        if return_val is None:
            return None, 400
        else:
            return {'name': return_val}, 200

    def post(self,iataCode):
        if len(iataCode) != 3:
            return None, 400

        if airports_util.airport_exist(iataCode):
            return None, 201

        parser = reqparse.RequestParser()
        parser.add_argument('name', location=["json", "form"])
        parser.add_argument('iataCode', location=["json", "form"])
        airport = parser.parse_args()

        
        airports_util.set_airport_name(airport)
        return None, 200
    

api.add_resource(AirportNames,f'{basePath}/airportName/<string:iataCode>')

if __name__=='__main__':
    app.run(host='127.0.0.1', debug = True)