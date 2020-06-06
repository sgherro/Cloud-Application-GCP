from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import InputRequired, Length

class AirportsForm(FlaskForm):
    name = StringField('Immettere un nome', validators = [InputRequired(), 
    Length(min=1,max =40, message=('Your message is too long, max 100')) ])
    iata_code = TextField('Codice Iata', validators = [InputRequired(), 
    Length(min=3,max =3, message=('Your message is too long, max 100')) ])
    submit = SubmitField('Inserisci')

class SearchAir(FlaskForm):
    search = TextField('Ricerca', validators = [InputRequired(), 
    Length(min=3,max =3, message=('Your message is too long, max 100')) ])
    submit = SubmitField('Cerca')
