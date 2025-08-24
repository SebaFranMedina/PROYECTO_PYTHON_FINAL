from fastapi import APIRouter, HTTPException, Form
from datetime import datetime
from app.core.prestamos import db_prestamos
from app.core.usuarios import db_usuarios
from app.core.libros import db_libros

router = APIRouter(prefix="/api/prestamos", tags=["Préstamos"])

# Crear préstamo
# Crear préstamo
@router.post("/")
def crear_prestamo(
    email: str = Form(...),
    libro_id: int = Form(...),
    fecha_prestamo: str = Form(...),
    fecha_devolucion_esperada: str = Form(...)
):
    # Buscar usuario por email
    usuario = next((u for u in db_usuarios.get_todos() if u.email == email), None)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"No se encontró usuario con email {email}")

    # Validar que el usuario esté activo
    if usuario.estado.nombre.lower() in ["suspendido", "inactivo"]:
        raise HTTPException(
            status_code=403,
            detail=f"El usuario {usuario.nombre} {usuario.apellido} está {usuario.estado.nombre} y no puede tomar préstamos"
        )

    # Buscar libro
    libro = db_libros.get_por_id(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail=f"No se encontró libro con ID {libro_id}")
    if getattr(libro, "estado", "Disponible") != "Disponible":
        raise HTTPException(status_code=400, detail="El libro no está disponible")

    # Convertir fechas
    try:
        fecha_prestamo_dt = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
        fecha_devolucion_dt = datetime.strptime(fecha_devolucion_esperada, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=422, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    # Crear préstamo
    prestamo = db_prestamos.crear(
        usuario_id=usuario.usuario_id,
        libro_id=libro_id,
        fecha_prestamo=fecha_prestamo_dt,
        fecha_devolucion_esperada=fecha_devolucion_dt
    )

    # Actualizar estado del libro
    libro.estado = "Prestado"

    return {"message": "Préstamo creado", "prestamo_id": prestamo.prestamo_id}


# Finalizar préstamo
@router.post("/{prestamo_id}/finalizar")
def finalizar_prestamo(prestamo_id: int):
    prestamo = db_prestamos.finalizar(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail=f"No se encontró préstamo con ID {prestamo_id}")

    # Cambiar estado del libro
    libro = db_libros.get_por_id(prestamo.libro_id)
    if libro:
        libro.estado = "Disponible"

    return {"message": "Préstamo finalizado", "prestamo_id": prestamo.prestamo_id}

# Marcar como perdido
@router.post("/{prestamo_id}/perdido")
def perdido_prestamo(prestamo_id: int):
    prestamo = db_prestamos.marcar_perdido(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail=f"No se encontró préstamo con ID {prestamo_id}")

    return {"message": "Préstamo marcado como perdido", "prestamo_id": prestamo.prestamo_id}
