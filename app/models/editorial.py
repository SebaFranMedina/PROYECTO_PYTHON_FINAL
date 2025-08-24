from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Editorial(Base):
    __tablename__ = 'editoriales'
    editorial_id = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False)
    direccion = Column(Text, nullable=True)
    telefono = Column(Text, nullable=True)
    email = Column(Text, nullable=True)

    # Relación inversa con Libro
    libros = relationship("Libro", back_populates="editorial")

    def __repr__(self):
        return self.nombre
