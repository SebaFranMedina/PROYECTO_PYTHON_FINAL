from app.core.database import SessionLocal
from app.models.rol import Rol

class GestorRoles:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self, order_by: str = "id"):
        """Devuelve todos los roles ordenados por la columna especificada"""
        if order_by == "id":
            columna = Rol.rol_id
        elif order_by == "nombre":
            columna = Rol.nombre
        else:
            raise ValueError(f"Columna desconocida para ordenar: {order_by}")

        return self.session.query(Rol).order_by(columna).all()

    def get_por_id(self, rol_id: int):
        """Obtiene un rol por su ID"""
        return self.session.query(Rol).get(rol_id)

    def crear(self, datos_rol: dict):
        """Crea un nuevo rol"""
        nuevo = Rol(**datos_rol)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
            return nuevo
        except Exception as e:
            self.session.rollback()
            print(f"Error al crear rol: {e}")
            return None

    def actualizar(self, rol_id: int, actualizacion: dict):
        """Actualiza un rol existente"""
        rol = self.session.query(Rol).get(rol_id)
        if not rol:
            return None
        for campo, valor in actualizacion.items():
            setattr(rol, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(rol)
            return rol
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar rol: {e}")
            return None

    def eliminar(self, rol_id: int):
        """Elimina un rol por su ID"""
        rol = self.session.query(Rol).get(rol_id)
        if not rol:
            return None
        try:
            self.session.delete(rol)
            self.session.commit()
            return rol
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar rol: {e}")
            return None

# Instancia global para usar en el router
db_roles = GestorRoles()
