from app.core.database import SessionLocal
from app.models.libros import Libro

class GestorLibros:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        """Devuelve todos los libros ordenados por ID"""
        return self.session.query(Libro).order_by(Libro.libro_id).all()

    def get_por_id(self, libro_id: int):
        """Devuelve un libro por su ID"""
        return self.session.query(Libro).get(libro_id)

    def crear(self, datos_libro: dict):
        """Crea un nuevo libro"""
        nuevo = Libro(**datos_libro)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nuevo

    def actualizar(self, libro_id: int, actualizacion: dict):
        """Actualiza un libro existente"""
        libro = self.session.query(Libro).get(libro_id)
        if not libro:
            return None
        for campo, valor in actualizacion.items():
            setattr(libro, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(libro)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return libro

    def eliminar(self, libro_id: int):
        """Elimina un libro por su ID (solo si no tiene préstamos)"""
        libro = self.session.query(Libro).get(libro_id)
        if not libro:
            return None
        # 🚫 Bloqueo: no se puede borrar si tiene préstamos
        if hasattr(libro, "prestamos") and libro.prestamos:
            raise ValueError("No se puede eliminar un libro con préstamos asociados")
        try:
            self.session.delete(libro)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            raise
        return libro


# Instancia global del gestor
db_libros = GestorLibros()
