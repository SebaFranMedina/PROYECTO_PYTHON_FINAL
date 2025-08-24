from app.core.database import SessionLocal
from app.models.categoria import Categoria

class GestorCategorias:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self, order_by=None):
        """Obtiene todas las categorías, con ordenamiento opcional"""
        query = self.session.query(Categoria)
        if order_by:
            query = query.order_by(order_by)
        return query.all()

    def get_por_id(self, categoria_id: int):
        return self.session.query(Categoria).get(categoria_id)

    def crear(self, datos_categoria: dict):
        nuevo = Categoria(**datos_categoria)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return nuevo

    def actualizar(self, categoria_id: int, actualizacion: dict):
        categoria = self.session.query(Categoria).get(categoria_id)
        if not categoria:
            return None
        for campo, valor in actualizacion.items():
            setattr(categoria, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(categoria)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return categoria

    def eliminar(self, categoria_id: int):
        categoria = self.session.query(Categoria).get(categoria_id)
        if not categoria:
            return None
        try:
            self.session.delete(categoria)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        return categoria

db_categorias = GestorCategorias()
