from flask import Flask, render_template, request
from forms import myForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3esacosdncwefn3rif3ufcs'

@app.route('/greetings', methods=['POST'])
def greeting_link():
    #prima c'era request.form['greeting_name'] come nome della variabile richiesta
    #ora il nome è entry per via della struttura della form myForm
    recipient = request.form["entry"]
    #recipient = request.form['greeting_name']
    return render_template('greeting_link.html', recipient = recipient)
    

@app.route('/greetings', methods=['GET'])
def greeting_page():
    form = myForm()
    return render_template('form.html', form = form)
    #return render_template('greeting_form.html')

@app.route('/greetings/<recipient>', methods=['GET']) 
# guarda nel template di recipient cosa viene scritto nell'url
def hello(recipient):
    return render_template('greetings.html', recipient=recipient)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


#main
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)