from google.cloud import firestore

db = firestore.Client()
price_ref = db.collection(u'price')


class Price(object):
    def __init__(self):
        pass

    def get_object(self, user_uuid, object_id):
        try:
            ref = price_ref.document(object_id).get().to_dict()['items']
            for r in ref:
                if r['user_uuid'] == user_uuid:
                    return r
            return None
        except Exception:
            return None

    def post_object(self, user_uuid, object_id, percentage):
        ref = price_ref.document(object_id)
        try:
            ref.update({
                'items': firestore.ArrayUnion([{
                    'user_uuid' : user_uuid,
                    'percentage': percentage
                }])
            })
        except Exception:
            ref.set({
                'items':firestore.ArrayUnion([{
                    'user_uuid' : user_uuid,
                    'percentage': percentage
                }])
            })
    
    def get_details(self, object_id):
        try:
            ref = price_ref.document(object_id).get().to_dict()
            return ref
        except Exception:
            return None
    
    def get_list(self, user):
        objects = price_ref.get()
        ret = []
        for obj in objects:
            ref = price_ref.document(obj.id).get().to_dict()['items']
            for r in ref:
                if r['user_uuid'] == user:
                    c = {
                        'object_uri':obj.id,
                        'percentage': r['percentage']
                    }
                    ret.append(c)
        
        return ret
