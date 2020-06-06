from flask import abort, jsonify
from google.cloud import firestore

def api_visits(request):
    db = firestore.Client(project='airports-project')
    if request.method == 'GET':
        docs = db.collection(u'visits').stream()
        ret = {d.id: d.to_dict() for d in docs}
        return jsonify(ret)
    if request.method == 'POST':
        content_type = request.headers['content-type']
        if content_type == 'application/json':
            request_json = request.get_json(silent=True)
            if request_json and 'page' in request_json:
                page_name = request_json['page']
            else:
                raise ValueError("JSON is invalid or missing a 'page' property")
            if request_json and 'visits' in request_json:
                count_val = request_json['visits']
            else:
                raise ValueError("JSON is invalid or missing a 'visits' property")
        counter_ref = db.collection(u'visits').document(f'{page_name}')
        counter_ref.set({u'counter': count_val})
        return '', 200
