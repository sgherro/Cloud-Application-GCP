from flask import Flask, render_template
from google.cloud import firestore
from datetime import datetime
import requests
import statistics

app = Flask(__name__)
db = firestore.Client()
price_ref = db.collection(u'price')

def get_list(user):
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

@app.route('/', methods=['GET'])
def index():
    objects = price_ref.get()
    list_user = {}
    for obj in objects:
        users = price_ref.document(obj.id).get().to_dict()['items']
        for user in users:
            if user['user_uuid'] not in list_user:
                list_user[user['user_uuid']] = {
                    'items': get_list(user['user_uuid'])
                }
            else:
                list_user[user['user_uuid']].update({
                'items': get_list(user['user_uuid'])
            })
    return render_template('index.html', list_user=list_user)

@app.route('/statistics', methods=['GET'])
def stat():
    objects = price_ref.get()
    list_user = []
    list_sconti = []
    num_oggetti = 0
    for obj in objects:
        users = price_ref.document(obj.id).get().to_dict()['items']
        for user in users:
            num_oggetti += 1
            if user['user_uuid'] not in list_user:
                list_user.append(user['user_uuid'])
            list_sconti.append(user['percentage'])

    num_utenti = len(list_user)
    num_oggetti /= num_utenti
    scontistica = statistics.mean(list_sconti)
    return render_template('stat.html', num_utenti=num_utenti,
     num_oggetti=num_oggetti, scontistica= scontistica)

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
