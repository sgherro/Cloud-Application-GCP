from flask import Flask, render_template, Flask, request
from google.cloud import firestore
from datetime import datetime
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
db = firestore.Client()
mc = db.collection(u'musicCatalog')
genres = [('rock', 'rock'), ('pop', 'pop'), ('electronic', 'electronic'), ('dance', 'dance')]

class genreForm(FlaskForm):
    genre = SelectField('Genre', choices=genres)
    submit = SubmitField('Submit')

@app.route('/', methods = ['GET'])
def index():
    ref = mc.get()
    list_artist = {}
    for x in ref:
        artist = x.to_dict()['name']
        if artist not in list_artist:
            list_artist[artist] = {}
            disc_list = mc.document(x.id).collection(u'DiscInfo').get()
            for d in disc_list:
                if d.id not in list_artist[artist]:
                    list_artist[artist][d.id] = {}
                list_artist[artist][d.id] = d.to_dict()  

    return render_template("index.html", list_artist=list_artist)

@app.route('/search', methods = ['GET'])
def search_genre():  
    form = genreForm()
    return render_template("search.html", form = form)

@app.route('/search', methods = ['POST'])
def search_genre_post():
    form = genreForm()
    genre = request.form['genre']
    r = requests.get(f"https://api-dot-music-sac1203.ew.r.appspot.com/api/v1/genre/{genre}")
    list_disc = r.json()
    return render_template("search.html", list_disc=list_disc, form=form)
                
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    return datetime.strptime(date, '%d%m%Y').strftime("%Y/%m/%d")

if __name__ =='__main__':
    app.run('127.0.0.1', port = 8080, debug = True)