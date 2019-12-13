from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

class addEtudiant(FlaskForm):
    nom=StringField('nom')
    nom=StringField('CNE')
    RFID=StringField('RFID',id='RFID')
    submit = SubmitField('Ajouter')
