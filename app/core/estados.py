from app.core.database import SessionLocal
from app.models.estados_usuario import Estado  # importamos la clase correcta


class GestorEstados:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self, order_by: str = "id"):
        """Devuelve todos los estados ordenados por la columna especificada"""
        if order_by == "id":
            columna = Estado.estado_usuario_id  # ⚠️ No 'estado_id'
        elif order_by == "nombre":
            columna = Estado.nombre
        else:
            raise ValueError(f"Columna desconocida para ordenar: {order_by}")

        return self.session.query(Estado).order_by(columna).all()

    def get_por_id(self, estado_usuario_id: int):
        """Obtiene un estado por su ID"""
        return self.session.query(Estado).get(estado_usuario_id)

    def crear(self, datos_estado: dict):
        """Crea un nuevo estado"""
        nuevo = Estado(**datos_estado)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
            return nuevo
        except Exception as e:
            self.session.rollback()
            print(f"Error al crear estado: {e}")
            return None

    def actualizar(self, estado_usuario_id: int, actualizacion: dict):
        """Actualiza un estado existente"""
        estado = self.session.query(Estado).get(estado_usuario_id)
        if not estado:
            return None
        for campo, valor in actualizacion.items():
            setattr(estado, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(estado)
            return estado
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar estado: {e}")
            return None

    def eliminar(self, estado_usuario_id: int):
        """Elimina un estado por su ID"""
        estado = self.session.query(Estado).get(estado_usuario_id)
        if not estado:
            return None
        try:
            self.session.delete(estado)
            self.session.commit()
            return estado
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar estado: {e}")
            return None


# instancia global para usar en el router
db_estados = GestorEstados()
