from flask import Flask, render_template, request
from google.cloud import firestore
from dateutil.parser import parse
from google.cloud.firestore_v1 import ArrayUnion
from forms import myForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3esacosdncwefn3rif3ufcs'
#remember $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\simof\project_sac\SimpleFlaskApp\keysgcp.json"
db = firestore.Client()
index_ref = db.collection(u'index').document(u'last_access')
greetings_ref = db.collection(u'greetings')

@app.route('/greetings', methods=['POST'])
def greeting_link():
    #prima c'era request.form['greeting_name'] come nome della variabile richiesta
    #ora il nome è entry per via della struttura della form myForm
    recipient = request.form["entry"]
    #recipient = request.form['greeting_name']
    docs = greetings_ref.stream()
    try:
        date = greetings_ref.document(recipient).get().to_dict()['ListaAccessi']
    except Exception:
        date = datetime.datetime.utcnow()
    for doc in docs:#visualizza tutti i documenti nella collection
        print(doc.to_dict()[u'ListaAccessi'])
    return render_template('greeting_link.html', recipient = recipient, date = date)

@app.route('/greetings', methods=['GET'])
def greeting_page():
    form = myForm()
    return render_template('form.html', form = form)
    #return render_template('greeting_form.html')

@app.route('/greetings/<recipient>', methods=['GET']) 
# guarda nel template di recipient cosa viene scritto nell'url
def hello(recipient):
    #greetings_rec_ref=db.collection(recipient).document(u'access')
    rec_ref = greetings_ref.document(recipient)
    date = datetime.datetime.utcnow()
    date = parse(str(date))
    date= date.strftime("%H:%M:%S,%Y/%m/%d")
    try:
        rec_ref.update({
            u'ListaAccessi': firestore.ArrayUnion([str(date)])
        })
    except Exception:
        rec_ref.set({
            u'ListaAccessi': firestore.ArrayUnion([str(date)])
        }) 
    date = rec_ref.get().to_dict()['ListaAccessi']
    return render_template('greetings.html', recipient=recipient, date=date)

@app.route('/', methods=['GET'])
def index():
    index_ref.set({
        u'Ultimo_accesso': firestore.SERVER_TIMESTAMP
    })
    date = index_ref.get().to_dict()['Ultimo_accesso']
    date = parse(str(date))
    date= date.strftime("%H:%M:%S,%Y/%m/%d")
    return render_template('index.html', date=date)

#main
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
