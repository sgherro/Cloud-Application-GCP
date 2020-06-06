from google.cloud import firestore
from flask import request, Flask

#remember $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\simof\project_sac\SimpleFlaskApp\keysgcp.json"
db = firestore.Client()
airports_ref = db.collection(u'airports')

class Airports(object):
    def __init__(self):
       pass
    
    def get_airport_by_iata(self,iata_code):
        airport_dict = airports_ref.document(iata_code).get().to_dict()
        if airport_dict is None:
            return None
        return airport_dict['name']
    
    def airport_exist(self, iataCode):
        return airports_ref.document(iataCode).get().exists

    def set_airport_name(self,airport):
        if len(airport["iataCode"]) != 3:
            return False
        airports_ref.document(airport["iataCode"]).set({
                u'name':airport["name"],
            })
        return True

    