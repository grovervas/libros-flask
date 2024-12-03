from app import db
from sqlalchemy.orm import Mapped, mapped_column

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
            f'Tópico: {self.topico}'            
        )