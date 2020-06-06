from google.cloud import firestore

db = firestore.Client()
cinema_ref = db.collection(u'cinema')

class Cinema(object):
    def __init__(self):
        pass

    def post_booking(self, date, time, seat):
        if seat is None:
            return None

        try:
            cinema_ref.document(f'{date}T{time}').update({
                'postiPrenotati' : firestore.ArrayUnion([seat])
            })
        except Exception:
            cinema_ref.document(f'{date}T{time}').set({
                'postiPrenotati' : firestore.ArrayUnion([seat])
            })
        

    def get_booking(self, date, time):

        try:
            ref = cinema_ref.document(f'{date}T{time}').get()
            ref = ref.to_dict()['postiPrenotati']
            print(ref)
        except Exception:
            ref = []
        return ref

    def get_date(self, date):
        ret_value = []
        for time in ['19:30','21:30','22:30']:
            ref = cinema_ref.document(f'{date}T{time}').get()
            if ref.exists:
                r = {}
                r = ref.to_dict()
                r['time'] = time
                ret_value.append(r)

        return ret_value
