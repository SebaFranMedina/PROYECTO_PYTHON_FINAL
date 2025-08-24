from pydantic import BaseModel
from datetime import datetime

class PrestamoBase(BaseModel):
    libro_id: int
    usuario_id: int
    fecha_prestamo: datetime
    fecha_devolucion_esperada: datetime
    estado: str

class Prestamo(PrestamoBase):
    prestamo_id: int

    model_config = {
        "from_attributes": True
    }
