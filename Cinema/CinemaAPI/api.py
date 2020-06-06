from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from cinema import Cinema
from datetime import datetime


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'e3esacosdncwefn3rif3ufcs'

basePath = '/api/v1' #uguale a quello nel file .yaml
c = Cinema()

# validatori dei parametri, data e time
def validDate(date):
    try:
        datetime.strptime(date, '%d%m%Y')
        return True
    except ValueError:
        return False

def validTime(time):
    if time in ['19:30','21:00','22:30']:
        return True
    return False


# convertiamo seat in in numero e viceversa

def SeatToInt(seat):
    return (ord(str.upper(seat['row'])) - ord('A')) * 10 + seat['seat']

def IntToSeat(val):
    return {'row': chr(ord('A') + int(val)//10), 'seat': int(val) % 10}

class Booking(Resource):

    def post(self, date, time):
    #PostBooking
        print("POST")
        if not validDate(date):
            return None, 400
        
        if not validTime(time):
            return None, 404
        try:
            r = request.get_json()
            req_seat = []
            for s in r['items']:
                req_seat.append(SeatToInt(s))
        
            booked_seat = c.get_booking(date,time)
        
            if req_seat in booked_seat:
                return None, 409

            for seat in req_seat:
                c.post_booking(date, time, seat)
            return None, 201
        except Exception:
            return None, 400
        
    def get(self, date, time):
    #GetBooking
        if not validTime(time) or not validDate(date):
            
            return None, 404
        ref = c.get_booking(date, time)
        if ref is not None:
            return {'items': [IntToSeat(r) for r in ref]}, 200
        return None, 404

class BookingDate(Resource):

    def get(self, date):

        if not validDate(date):
            return None, 400

        ref = c.get_date(date)
        ret_val = []
        for r in ref:
            print(r)
            ret = {}
            ret['time'] = r['time']
            ret['booked_seats'] = {
                'items': [IntToSeat(x) for x in r['postiPrenotati']]
            }
            ret_val.append(ret)
        return ret_val, 200        

class newBooking(Resource):

    def post(self, date, time):

        if not validDate(date):
            return None, 400
        if not validTime(time):
            return None, 404
        
        try:
            ref = request.get_json()
            num = ref['num']
            booked_seat = c.get_booking(date,time)
            req_seat = []

            if num + len(booked_seat) > 100:
                return None, 409
            mid = 5
            while mid < 100:
                r = set(list(range(mid - num // 2, mid + num // 2)))
                if r - set(booked_seat) == r:
                    for x in r:
                        c.post_booking(date, time, x)
                    return None, 201
                else:
                    mid += 10
            return None, 400
        except Exception:
            return None, 400


api.add_resource(Booking, f'{basePath}/books/<string:date>/<string:time>')
api.add_resource(BookingDate, f'{basePath}/book/<string:date>')
api.add_resource(newBooking, f'{basePath}/auto/<string:date>/<string:time>')


if __name__=='__main__':
    app.run(host='127.0.0.1', debug = True)