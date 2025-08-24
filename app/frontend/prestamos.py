from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path
from datetime import datetime, date


from app.core.database import get_db
from app.models.usuarios import Usuario
from app.models.libros import Libro
from app.models.prestamos import Prestamo

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent / "templates")

# -----------------
# Listar préstamos
# -----------------
@router.get("/prestamos")
async def list_prestamos(request: Request, db: Session = Depends(get_db)):
    prestamos = db.query(Prestamo).all()
    prestamos_list = []

    for prestamo in prestamos:
        multa = prestamo.multa
        # Priorizar estado real del préstamo
        if prestamo.estado == "completado":
            estado_mostrar = "completado"
        elif prestamo.estado == "perdido":
            estado_mostrar = "perdido"
        else:
            # Si aún no devolvió o se devolvió tarde
            if prestamo.fecha_devolucion_real:
                dias_mora = (prestamo.fecha_devolucion_real.date() - prestamo.fecha_devolucion_esperada.date()).days
                if dias_mora > 0:
                    multa = 15000
                    estado_mostrar = "atrasado"
                else:
                    estado_mostrar = prestamo.estado
            else:
                dias_mora = (date.today() - prestamo.fecha_devolucion_esperada.date()).days
                if dias_mora > 0:
                    multa = 15000
                    estado_mostrar = "atrasado"
                else:
                    estado_mostrar = prestamo.estado

        prestamos_list.append({
            "prestamo": prestamo,
            "multa": multa,
            "estado": estado_mostrar
        })

    return templates.TemplateResponse(
        "prestamos/list.html",
        {"request": request, "prestamos": prestamos_list}
    )




# -----------------
# Crear préstamo (GET/POST)
# -----------------
@router.get("/prestamos/create")
async def create_prestamo_form(request: Request, db: Session = Depends(get_db)):
    # Solo usuarios con estado "Activo" (ajustá mayúsculas según tu tabla)
    usuarios = (
        db.query(Usuario)
        .join(Usuario.estado)
        .filter(Usuario.estado.has(nombre="Activo"))
        .all()
    )

    # Solo libros con ejemplares disponibles
    libros = db.query(Libro).filter(Libro.ejemplares_disponibles > 0).all()

    return templates.TemplateResponse(
        "prestamos/create.html",
        {"request": request, "usuarios": usuarios, "libros": libros}
    )



@router.post("/prestamos/create")
async def create_prestamo_submit(
    request: Request,
    usuario_id: int = Form(...),
    libro_id: int = Form(...),
    fecha_prestamo: str = Form(...),
    fecha_devolucion: str = Form(...),
    db: Session = Depends(get_db)
):
    fecha_prestamo_dt = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
    fecha_devolucion_dt = datetime.strptime(fecha_devolucion, "%Y-%m-%d")

    libro = db.query(Libro).filter(Libro.libro_id == libro_id).first()
    if not libro or libro.ejemplares_disponibles <= 0:
        return RedirectResponse("/prestamos/create", status_code=303)

    nuevo_prestamo = Prestamo(
        usuario_id=usuario_id,
        libro_id=libro_id,
        fecha_prestamo=fecha_prestamo_dt,
        fecha_devolucion_esperada=fecha_devolucion_dt,
        estado="activo",
        multa=0
    )
    db.add(nuevo_prestamo)
    libro.ejemplares_disponibles -= 1
    db.commit()
    return RedirectResponse("/prestamos", status_code=303)

# -----------------
# Finalizar préstamo
# -----------------

@router.post("/prestamos/{prestamo_id}/finalizar")
async def finalizar_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.prestamo_id == prestamo_id).first()
    if not prestamo:
        return RedirectResponse("/prestamos?error=No+existe+prestamo", status_code=303)

    # Fecha de hoy
    fecha_real = datetime.now().date()  # solo date para comparar con fecha_devolucion_esperada.date()
    fecha_esperada = prestamo.fecha_devolucion_esperada.date()

    dias_mora = (fecha_real - fecha_esperada).days

    if dias_mora > 0:
        prestamo.estado = "atrasado"
        prestamo.multa = 15000
    else:
        prestamo.estado = "completado"
        prestamo.multa = 0

    prestamo.fecha_devolucion_real = fecha_real

    # actualizar stock del libro
    libro = db.query(Libro).filter(Libro.libro_id == prestamo.libro_id).first()
    if libro:
        libro.ejemplares_disponibles += 1

    db.commit()
    db.refresh(prestamo)

    return RedirectResponse("/prestamos?ok=Prestamo+finalizado", status_code=303)



# Marcar préstamo perdido
@router.post("/prestamos/{prestamo_id}/perdido")
async def prestamo_perdido(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.prestamo_id == prestamo_id).first()
    if not prestamo:
        return RedirectResponse("/prestamos", status_code=303)

    prestamo.estado = "perdido"
    prestamo.multa = 100000

    libro = db.query(Libro).filter(Libro.libro_id == prestamo.libro_id).first()
    if libro:
        libro.ejemplares_disponibles = max(0, libro.ejemplares_disponibles)

    db.commit()
    db.refresh(prestamo)
    return RedirectResponse("/prestamos", status_code=303)


# -----------------
# Eliminar préstamo
# -----------------
@router.post("/prestamos/{prestamo_id}/eliminar")
async def eliminar_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.prestamo_id == prestamo_id).first()
    if not prestamo:
        return RedirectResponse("/prestamos", status_code=303)

    if prestamo.estado in ["activo", "atrasado"]:
        db.query(Libro).filter(Libro.libro_id == prestamo.libro_id).update({
            "ejemplares_disponibles": Libro.ejemplares_disponibles + 1
        })

    db.delete(prestamo)
    db.commit()
    return RedirectResponse("/prestamos", status_code=303)
