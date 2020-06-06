

from flask import Flask, render_template, request
from google.cloud import firestore
from dateutil.parser import parse
from google.cloud.firestore_v1 import ArrayUnion
from forms_room import *
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3esacosdncwefn3rif3ufcs'
#remember $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\simof\project_sac\SimpleFlaskApp\keysgcp.json"
db = firestore.Client()
rooms_ref = db.collection(u'rooms')

@app.route('/', methods=['GET','POST'])
def index():
    rList = ['Room A','Room B','Room C']
    room_ref = rooms_ref.document('ciao')
    return render_template('index_page.html',room_list=rList)

@app.route('/<room>', methods=['GET'])
def rooms(room):
    form = RoomForm()
    return render_template('form_room.html', form = form)

@app.route('/<room>',methods=['POST'])
def new_msg(room):
    form = RoomForm()
    room_ref= rooms_ref.document(room).collection(u'messages')
 #try: #prendo il numero di messaggi
  #      msg_num = rooms_ref.document(u'1') # da sistemare
   # except Exception:
    msg_num =  'M-' + str(datetime.datetime.utcnow())
    utente = request.form["name"]
    if(utente==""):
        utente = "Anonymous"  
    messaggio = request.form['msg']
    msg_ref = room_ref.document(msg_num)
    msg_ref.set({
        u'Utente': utente,
        u"Messaggio": messaggio,
        u'Time': firestore.SERVER_TIMESTAMP
    })
    docs = room_ref.order_by(u'Time', direction = firestore.Query.DESCENDING).limit(10).stream()
    mList =[]
    i=0
    for doc in docs:
        i +=1
        u=doc.to_dict()[u'Utente']
        m=doc.to_dict()[u'Messaggio']
        mList.append(f'#{i} ({u}): {m}')

    return render_template('form_room.html',form=form, room=room, 
    viewMsg=mList)

#main
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)