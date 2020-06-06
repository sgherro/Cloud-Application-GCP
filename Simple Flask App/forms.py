from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class myForm(FlaskForm):
    entry = StringField('Immettere una stringa', validators=[InputRequired()])
    submit = SubmitField()

