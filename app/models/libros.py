# app/models/libros.py
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Libro(Base):
    __tablename__ = 'libros'

    libro_id = Column(Integer, primary_key=True)
    titulo = Column(Text, nullable=False)
    autor_id = Column(Integer, ForeignKey('autores.autor_id'))
    editorial_id = Column(Integer, ForeignKey('editoriales.editorial_id'))
    isbn = Column(Text, nullable=True)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'))
    cantidad_ejemplares = Column(Integer, nullable=False)
    ejemplares_disponibles = Column(Integer, nullable=False)
    ubicacion_id = Column(Integer, ForeignKey('ubicaciones.ubicacion_id'))
    resumen = Column(Text, nullable=True)

    # Relaciones
    autor = relationship("Autor", back_populates="libros")
    editorial = relationship("Editorial", back_populates="libros")
    categoria = relationship("Categoria", back_populates="libros")
    ubicacion = relationship("Ubicacion", back_populates="libros")
    prestamos = relationship(
        "Prestamo",
        back_populates="libro",
        cascade="all, delete-orphan",  # 🚀 Borra automáticamente los préstamos al borrar el libro
        passive_deletes=True
    )

    def __repr__(self):
        return f"{self.titulo} (ISBN: {self.isbn})"
