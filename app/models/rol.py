from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Rol(Base):
    __tablename__ = 'roles'
    rol_id = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False)

    # Relación inversa con Usuario
    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        return self.nombre
