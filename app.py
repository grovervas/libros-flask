#mkdir myproject, cd project, py -3 -m venv .venv
#.venv\Scripts\activate

#pip install flask
#pip install psycopg2-binary
#pip install flask-sqlalchemy
#pip install flask-migrate

#pip installa flask-wtf

from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import Mapped, mapped_column
from flask_migrate import Migrate

#importaciones 2
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
#from wtforms.validators import DataRequired
from database import db

from models import Curso
from forms import CursoForm

#Creamos la BD antes y luego nos conectamos
app = Flask(__name__)

USER_DB = 'postgres'
PASS_DB = '1234'
SERVER_DB = 'localhost'
NAME_DB = 'demo'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{SERVER_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB

#evitar relacion circular
#db = SQLAlchemy(app)
db.init_app(app)

#Migrate despues de la clase
migrate = Migrate()
migrate.init_app(app, db)

#comando:
#flask db init, flask db migrate, flask db upgrade
#flask db stamp head

#configurar flask-wtf
app.config['SECRET_KEY']='llave_secreta'


@app.route('/')
def inicio():
    #cursos = Curso.query.all()
    cursos = Curso.query.order_by('id')
    total_cursos = Curso.query.count()
    app.logger.debug(f'Listado de cursos: {cursos}')    
    return render_template('index.html', datos=cursos, total=total_cursos)

@app.route('/curso/<int:id>')
def ver_curso(id):
    #curso = Curso.query.get(id)
    curso = Curso.query.get_or_404(id)
    return render_template('curso.html', dato = curso)    

@app.route('/insertar-curso', methods=['GET', 'POST'])
def insertar_curso():
    curso = Curso() #Refactorizar
    cursoForm = CursoForm(obj=curso)
    if request.method == 'POST':
        if cursoForm.validate_on_submit():
            cursoForm.populate_obj(curso)
            app.logger.debug(f'Curso: {curso}')
            #Insertar registro
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('inicio'))
        
    return render_template('insertar-curso.html', formulario = cursoForm)

@app.route('/editar-curso/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    curso = Curso.query.get_or_404(id)
    #curso = Curso.query.get(id)
    cursoForm = CursoForm(obj=curso)
    if request.method == 'POST':
        if cursoForm.validate_on_submit():
            cursoForm.populate_obj(curso)
            app.logger.debug(f'Curso a actualizar: {curso}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar-curso.html', formulario = cursoForm)

@app.route('/eliminar-curso/<int:id>')
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('inicio'))