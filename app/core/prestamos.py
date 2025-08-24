from datetime import datetime
from typing import List, Optional
from app.models.prestamos import Prestamo
from app.core.database import SessionLocal

class GestorPrestamos:
    def __init__(self):
        self.db = SessionLocal()

    def get_todos(self) -> List[Prestamo]:
        return self.db.query(Prestamo).all()

    def get_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        return self.db.query(Prestamo).filter(Prestamo.prestamo_id == prestamo_id).first()

    def crear(self, usuario_id: int, libro_id: int, fecha_prestamo: datetime, fecha_devolucion_esperada: datetime) -> Prestamo:
        nuevo = Prestamo(
            usuario_id=usuario_id,
            libro_id=libro_id,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion_esperada=fecha_devolucion_esperada,
            fecha_devolucion_real=None,
            estado="Prestado",   # ← default inicial
            multa=0,
            notas=None
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def finalizar(self, prestamo_id: int):
        prestamo = self.get_por_id(prestamo_id)
        if prestamo and not prestamo.fecha_devolucion_real:
            prestamo.fecha_devolucion_real = datetime.now()
            prestamo.estado = "Devuelto"   # ← más claro que "D"
            self.db.commit()
            self.db.refresh(prestamo)
        return prestamo

    def marcar_perdido(self, prestamo_id: int):
        prestamo = self.get_por_id(prestamo_id)
        if prestamo and prestamo.estado != "Perdido":
            prestamo.fecha_devolucion_real = datetime.now()
            prestamo.estado = "Perdido"
            prestamo.multa = 100000
            self.db.commit()
            self.db.refresh(prestamo)
        return prestamo

db_prestamos = GestorPrestamos()
