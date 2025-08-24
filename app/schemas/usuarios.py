from pydantic import BaseModel


class UsuarioBase(BaseModel):
    dni: str
    nombre: str
    apellido: str
    email: str
    rol_id: int
    estado_id: int

class Usuario(UsuarioBase):
    usuario_id: int

    model_config = {
        "from_attributes": True
    }
