from app.core.database import SessionLocal
from app.models.editorial import Editorial

class GestorEditoriales:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self, order_by=None):
        query = self.session.query(Editorial)
        if order_by is not None:
            query = query.order_by(order_by)
        else:
            query = query.order_by(Editorial.editorial_id)
        return query.all()

    def get_por_id(self, editorial_id: int):
        return self.session.query(Editorial).get(editorial_id)

    def crear(self, datos_editorial: dict):
        nuevo = Editorial(**datos_editorial)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nuevo

    def actualizar(self, editorial_id: int, actualizacion: dict):
        editorial = self.session.query(Editorial).get(editorial_id)
        if not editorial:
            return None
        for campo, valor in actualizacion.items():
            setattr(editorial, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(editorial)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return editorial

    def eliminar(self, editorial_id: int):
        editorial = self.session.query(Editorial).get(editorial_id)
        if not editorial:
            return None
        try:
            self.session.delete(editorial)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return editorial

db_editoriales = GestorEditoriales()
