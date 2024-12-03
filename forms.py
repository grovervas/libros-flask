from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CursoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    instructor = StringField('Instructor', validators=[DataRequired()])
    topico = StringField('Tópico', validators=[DataRequired()])
    enviar = SubmitField('Enviar')