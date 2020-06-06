from flask import Flask, render_template
from google.cloud import firestore
from datetime import datetime
import requests

app = Flask(__name__)
db = firestore.Client()
note_ref = db.collection(u'note')

@app.route('/', methods=['GET'])
def index():
    owners = note_ref.get()
    list_owner = {}
    for owner in owners:
        if owner.id not in list_owner:
            list_owner[owner.id] = {}
            print(owner.id)
            note_list = note_ref.document(owner.id).collection(u'Note').get()
            for note in note_list:
                if note.id not in list_owner[owner.id]:
                    list_owner[owner.id][note.id] = {}
                list_owner[owner.id][note.id] = note.to_dict()
    return render_template('index.html', list_owner=list_owner)

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
