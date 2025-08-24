from app.core.database import SessionLocal
from app.models.ubicacion import Ubicacion

class GestorUbicaciones:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Ubicacion).order_by(Ubicacion.ubicacion_id).all()

    def get_por_id(self, ubicacion_id: int):
        return self.session.query(Ubicacion).get(ubicacion_id)

    def crear(self, datos_ubicacion: dict):
        nuevo = Ubicacion(**datos_ubicacion)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nuevo

    def actualizar(self, ubicacion_id: int, actualizacion: dict):
        ubicacion = self.session.query(Ubicacion).get(ubicacion_id)
        if not ubicacion:
            return None
        for campo, valor in actualizacion.items():
            setattr(ubicacion, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(ubicacion)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return ubicacion

    def eliminar(self, ubicacion_id: int):
        ubicacion = self.session.query(Ubicacion).get(ubicacion_id)
        if not ubicacion:
            return None
        try:
            self.session.delete(ubicacion)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return ubicacion

db_ubicaciones = GestorUbicaciones()
