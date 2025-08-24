from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Categoria(Base):
    __tablename__ = 'categorias'
    categoria_id = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False)

    # Relación inversa con Libro
    libros = relationship("Libro", back_populates="categoria")

    def __repr__(self):
        return self.nombre