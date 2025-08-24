from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    ubicacion_id = Column(Integer, primary_key=True)
    codigo = Column(Text, nullable=False)
    nombre = Column(Text, nullable=False)
    tipo = Column(Text, nullable=False)
    activo = Column(Integer, nullable=False)

    # Relación inversa hacia Libro
    libros = relationship("Libro", back_populates="ubicacion")
