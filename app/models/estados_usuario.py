from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Estado(Base):
    __tablename__ = "estados_usuarios"

    # ID del estado de usuario
    estado_usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Nombre del estado (único y obligatorio)
    nombre = Column(Text, nullable=False, unique=True)

    # Relación con la tabla Usuario
    usuarios = relationship(
        "Usuario",
        back_populates="estado"
    )

    def __repr__(self):
        return f"EstadoUsuario(id={self.estado_usuario_id}, nombre='{self.nombre}')"
