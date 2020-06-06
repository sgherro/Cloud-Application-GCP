from flask import Flask, render_template_string
# possiamo creare una struttura statiche della pagina html e flask può 
# automaticamente supportare le parti dinamiche della pagina, in maniera tale da renderla dinamica

#parte con il template
hello_template='''
                <html>
                <body><h1>Hello World, template mode {{recipient}}</h1></body
                </html>
                '''
app = Flask(__name__) #il nome dell'applicaione sarà uguale a quello del file usato, ovvero main.py

@app.route('/', methods=['GET']) 
# @ è un decoratore di flask, serve per sapere che la funzione hello() viene invocata
# quando si deve rispondere ad un metoodo GET nella directory root, /. 

def hello():
    #parte con template
    return render_template_string(hello_template,recipient='CIaoen')
    #prima parte senza template
    #return '<html><body><h1>Hello World</h1></body></html>'


#main
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
