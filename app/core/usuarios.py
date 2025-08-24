from app.core.database import SessionLocal
from app.models.usuarios import Usuario
from sqlalchemy.orm import joinedload

class GestorUsuarios:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        """Devuelve todos los usuarios ordenados por ID con relaciones cargadas"""
        return (
            self.session
            .query(Usuario)
            .options(
                joinedload(Usuario.estado),  # carga la relación estado
                joinedload(Usuario.rol)      # carga la relación rol
            )
            .order_by(Usuario.usuario_id)
            .all()
        )

    def get_por_id(self, usuario_id: int):
        """Devuelve un usuario por su ID"""
        return self.session.query(Usuario).get(usuario_id)

    def crear(self, datos_usuario: dict):
        """Crea un nuevo usuario"""
        nuevo = Usuario(**datos_usuario)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
            self.session.expire_all()  # refresca la sesión
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nuevo

    def actualizar(self, usuario_id: int, actualizacion: dict):
        """Actualiza un usuario existente"""
        usuario = self.session.query(Usuario).get(usuario_id)
        if not usuario:
            return None
        for campo, valor in actualizacion.items():
            setattr(usuario, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(usuario)
            self.session.expire_all()  # refresca la sesión
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return usuario

    def eliminar(self, usuario_id: int):
        """Elimina un usuario por su ID"""
        usuario = self.session.query(Usuario).get(usuario_id)
        if not usuario:
            return None
        try:
            self.session.delete(usuario)
            self.session.commit()
            self.session.expire_all()  # refresca la sesión
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return usuario

# Instancia global del gestor
db_usuarios = GestorUsuarios()
