
from flask import Flask, render_template, request,url_for,flash, redirect
from flask_restful import Resource
from form_airports import *
import requests 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3esacosdncwefn3rif3ufcs'

basePath = 'https://api-dot-airports-project.ew.r.appspot.com/api/v1' #uguale a quello nel file .yaml
#basePath = 'http://127.0.0.1:5000/api/v1'
funcPath = "https://us-central1-airports-project.cloudfunctions.net/http_visiting"
@app.route(f'/',methods = ['GET'])
def index():
    return render_template("index_airports.html")

@app.route(f'/search', methods =['GET'])    
def search():
    form = SearchAir()
    requests.post(funcPath,json={'page': 'search'})
    return render_template("search_airports.html",form = form)

@app.route(f'/search', methods = ['POST'])
def search_post():
    form = SearchAir()
    iataCode = request.form["search"]
    requests.post(funcPath,json={'page': 'search'})
    r = requests.get(f"{basePath}/airportName/{iataCode}")
    if r.status_code != 200:
        return render_template("search_airports.html",form=form,airport="Nessun aeroporto trovato!")    
    return render_template("search_airports.html", form = form, airport = r.json()['name'])

@app.route(f'/insert',methods = ['GET'])
def insert():
    form = AirportsForm()
    requests.post(funcPath,json={'page': 'insert'})
    return render_template('airport_form.html', form = form)
    
@app.route(f'/insert',methods = ['POST'])
def insert_post():
    form = AirportsForm()
    requests.post(funcPath,json={'page': 'insert'})
    name = request.form['name']
    iata_code = request.form['iata_code']
    airport = {
        'iataCode':iata_code,
        'name':name
    }

    if len(iata_code) != 3:
        flash(f"Invalid iata code: {airport['iataCode']}, airport {airport['name']} not posted")
        return redirect(url_for('insert'))
    else:
        r = requests.post(f"{basePath}/airportName/{iata_code}", airport)
       #così facendo faccio una richiesta post all'URI con il dict airport passato
        if r.status_code is not 200:
            flash(f"Invalid iata code: {airport['iataCode']}, airport {airport['name']} not posted")
        else:
            flash(f"Invalid iata code: {airport['iataCode']}, airport {airport['name']} not posted")
            return redirect(url_for('insert')) 
    return render_template('airport_form.html', title='Insert Airport', form=form)

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8080, debug = True)