#mkdir myproject, cd project, py -3 -m venv .venv
#.venv\Scripts\activate

#pip install flask
#pip install psycopg2-binary
#pip install flask-sqlalchemy
#pip install flask-migrate

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from flask_migrate import Migrate

#Creamos la BD antes y luego nos conectamos
app = Flask(__name__)

USER_DB = 'postgres'
PASS_DB = '1234'
SERVER_DB = 'localhost'
NAME_DB = 'demo'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{SERVER_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB

db = SQLAlchemy(app)

#Migrate despues de la clase
migrate = Migrate()
migrate.init_app(app, db)

#comando:
#flask db init, flask db migrate, flask db upgrade
#flask db stamp head


#Clase modelo
class Curso(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #nombre = db.Column(db.String(250))
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    instructor: Mapped[str]
    topico: Mapped[str]
    
    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'Curso: {self.nombre}, '
            f'Instructor: {self.instructor}, '
            f'topico: {self.topico}'            
        )

@app.route('/')
def inicio():
    cursos = Curso.query.all()
    total_cursos = Curso.query.count()
    app.logger.debug(f'Listado de cursos: {cursos}')    
    return render_template('index.html', datos=cursos, total=total_cursos)

    
