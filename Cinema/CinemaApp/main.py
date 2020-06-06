from flask import Flask, render_template
from google.cloud import firestore
from datetime import datetime

app = Flask(__name__)
db = firestore.Client()
cinema_ref = db.collection(u'cinema')

@app.route('/', methods = ['GET'])
def index():
    date_list = {}
    for x in cinema_ref.get():
        date, time = x.id.split('T')
        if date not in date_list:
            date_list[date] = {}
            l = len(x.to_dict()['postiPrenotati'])
        date_list[date][time] = l

    return render_template("index.html", date_list=date_list)


if __name__ =='__main__':
    app.run('127.0.0.1', port = 8080, debug = True)