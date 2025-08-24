# app/frontend/wikipedia.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.api.wikipedia import book_summary  # función que trae resumen desde Wikipedia

router = APIRouter(tags=["Frontend Wikipedia"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Vista Wikipedia de libros
@router.get("/libros/{libro_id}/wiki", response_class=HTMLResponse)
def libro_wikipedia(request: Request, libro_id: int):
    from app.core.libros import db_libros
    libro = db_libros.get_por_id(libro_id)
    if not libro:
        return HTMLResponse(content="Libro no encontrado", status_code=404)
    
    data = book_summary(libro.titulo)

    if not data or "extract" not in data:
        return templates.TemplateResponse(
            "libros/wiki_summary.html",
            {"request": request, "libro": libro, "data": None, "error": "No se encontró información en Wikipedia"}
        )
    
    return templates.TemplateResponse(
        "libros/wiki_summary.html",
        {"request": request, "libro": libro, "data": data}
    )

# Vista Wikipedia de autores
@router.get("/autores/{autor_id}/wiki", response_class=HTMLResponse)
def autor_wikipedia(request: Request, autor_id: int):
    from app.core.autores import db_autores
    autor = db_autores.get_por_id(autor_id)
    if not autor:
        return HTMLResponse(content="Autor no encontrado", status_code=404)

    nombre_completo = f"{autor.nombre} {autor.apellido}"
    data = book_summary(nombre_completo)  # reutilizamos la función para Wikipedia

    if not data or "extract" not in data:
        return templates.TemplateResponse(
            "autores/wiki_summary.html",
            {"request": request, "autor": autor, "data": None, "error": "No se encontró información en Wikipedia"}
        )

    return templates.TemplateResponse(
        "autores/wiki_summary.html",
        {"request": request, "autor": autor, "data": data}
    )
