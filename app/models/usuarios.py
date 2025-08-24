from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.rol import Rol


class Usuario(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True)
    dni = Column(Text, nullable=False)
    nombre = Column(Text, nullable=False)
    apellido = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.rol_id'))
    estado_id = Column(Integer, ForeignKey('estados_usuarios.estado_usuario_id'))

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    estado = relationship(
        "Estado",
        back_populates="usuarios",
        primaryjoin="Usuario.estado_id == Estado.estado_usuario_id"
    )
    prestamos = relationship("Prestamo", back_populates="usuario")  # Asumiendo que Prestamo existe

    def __repr__(self):
        return f"{self.apellido}, {self.nombre} - DNI: {self.dni}"
