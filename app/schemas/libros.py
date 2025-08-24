from pydantic import BaseModel
from typing import Optional

class LibroBase(BaseModel):
    titulo: str
    autor_id: int
    editorial_id: int
    isbn: Optional[str] = None
    categoria_id: int
    cantidad_ejemplares: int
    ejemplares_disponibles: Optional[int] = None
    ubicacion_id: int
    resumen: Optional[str] = None

class Libro(LibroBase):
    libro_id: int

    model_config = {
        "from_attributes": True
    }
