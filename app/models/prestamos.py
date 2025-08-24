# app/models/prestamos.py
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prestamo(Base):
    __tablename__ = 'prestamos'
    prestamo_id = Column(Integer, primary_key=True)
    libro_id = Column(Integer, ForeignKey('libros.libro_id', ondelete="CASCADE"))
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    fecha_prestamo = Column(DateTime, nullable=False)
    fecha_devolucion_esperada = Column(DateTime, nullable=False)
    fecha_devolucion_real = Column(DateTime, nullable=True)
    estado = Column(Text, nullable=False)
    multa = Column(Integer, nullable=True)
    notas = Column(Text, nullable=True)

    # Relaciones
    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")

    def __repr__(self):
        return f"Préstamo {self.prestamo_id} - Libro ID: {self.libro_id} - Estado: {self.estado}"
