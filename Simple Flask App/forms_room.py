from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import InputRequired, Length

class RoomForm(FlaskForm):
    name = StringField('Immettere un username')
    msg = TextField('Messaggio', validators = [InputRequired(), 
    Length(min=1,max =100, message=('Your message is too long, max 100')) ])
    submit = SubmitField('Invia')



