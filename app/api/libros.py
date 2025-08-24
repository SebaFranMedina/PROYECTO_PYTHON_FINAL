from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app.schemas.libros import Libro
from app.core.libros import db_libros  # <--- import actualizado

router = APIRouter(tags=["Libros API"])

@router.get("/libros/", response_model=list[Libro])
def listar_libros():
    return db_libros.get_todos()

@router.get("/libros/{libro_id}", response_model=Libro)
def obtener_libro(libro_id: int):
    libro = db_libros.get_por_id(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.post("/libros/", response_model=Libro)
def crear_libro(
    titulo: str = Form(...),
    autor_id: int = Form(...),
    editorial_id: int = Form(...),
    isbn: str = Form(...),
    categoria_id: int = Form(...),
    cantidad_ejemplares: int = Form(...),
    ejemplares_disponibles: int = Form(...),
    ubicacion_id: int = Form(...),
    resumen: str = Form(...)
):
    datos = {
        "titulo": titulo,
        "autor_id": autor_id,
        "editorial_id": editorial_id,
        "isbn": isbn,
        "categoria_id": categoria_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ejemplares_disponibles": ejemplares_disponibles,
        "ubicacion_id": ubicacion_id,
        "resumen": resumen
    }
    libro = db_libros.crear(datos)
    return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)

@router.post("/libros/{libro_id}/update", response_model=Libro)
def actualizar_libro(
    libro_id: int,
    titulo: str = Form(...),
    autor_id: int = Form(...),
    editorial_id: int = Form(...),
    isbn: str = Form(...),
    categoria_id: int = Form(...),
    cantidad_ejemplares: int = Form(...),
    ejemplares_disponibles: int = Form(...),
    ubicacion_id: int = Form(...),
    resumen: str = Form(...)
):
    datos = {
        "titulo": titulo,
        "autor_id": autor_id,
        "editorial_id": editorial_id,
        "isbn": isbn,
        "categoria_id": categoria_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ejemplares_disponibles": ejemplares_disponibles,
        "ubicacion_id": ubicacion_id,
        "resumen": resumen
    }
    libro = db_libros.actualizar(libro_id, datos)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)

@router.post("/libros/{libro_id}/eliminar", response_model=Libro)
def eliminar_libro(libro_id: int):
    try:
        libro = db_libros.eliminar(libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
    except ValueError as e:
        # Redirigir al listado con mensaje de error
        return RedirectResponse(url=f"/libros?error={str(e)}", status_code=HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)
