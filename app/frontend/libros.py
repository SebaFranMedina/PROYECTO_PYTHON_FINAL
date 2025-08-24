from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from starlette.status import HTTP_303_SEE_OTHER


from app.core.libros import db_libros
from app.core.editoriales import db_editoriales
from app.core.categorias import db_categorias
from app.core.ubicaciones import db_ubicaciones
from app.core.autores import db_autores


router = APIRouter(tags=["Frontend Libros"])

# 📌 Ruta absoluta a la carpeta de templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # sube hasta la raíz del proyecto
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ----------------------
# Listar todos los libros
# ----------------------
from fastapi import Request

@router.get("/libros", response_class=HTMLResponse)
async def list_libros(request: Request, error: str = None):
    libros = db_libros.get_todos()
    return templates.TemplateResponse(
        "libros/list.html",
        {
            "request": request,
            "libros": libros,
            "error": error  # agregamos el parámetro opcional
        }
    )


# ----------------------
# Mostrar formulario de creación de libro
# ----------------------
@router.get("/libros/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    autores = db_autores.get_todos()
    editoriales = db_editoriales.get_todos()
    categorias = db_categorias.get_todos()
    ubicaciones = db_ubicaciones.get_todos()
    return templates.TemplateResponse(
        "libros/create.html",
        {
            "request": request,
            "autores": autores,
            "editoriales": editoriales,
            "categorias": categorias,
            "ubicaciones": ubicaciones
        }
    )

# ----------------------
# Procesar creación de libro (POST)
# ----------------------
@router.post("/libros/create")
async def crear_libro(
    titulo: str = Form(...),
    isbn: str = Form(...),
    autor_id: int = Form(...),
    categoria_id: int = Form(...),
    editorial_id: int = Form(...),
    cantidad_ejemplares: int = Form(...),
    ubicacion_id: int = Form(...),
    resumen: str = Form(None)
):
    # 👇 asignamos automáticamente los ejemplares disponibles
    ejemplares_disponibles = cantidad_ejemplares

    nuevo_libro = {
        "titulo": titulo,
        "isbn": isbn,
        "autor_id": autor_id,
        "categoria_id": categoria_id,
        "editorial_id": editorial_id,
        "cantidad_ejemplares": cantidad_ejemplares,
        "ejemplares_disponibles": ejemplares_disponibles,
        "ubicacion_id": ubicacion_id,
        "resumen": resumen,
    }

    db_libros.crear(nuevo_libro)
    return RedirectResponse(url="/libros", status_code=HTTP_303_SEE_OTHER)

# ----------------------
# Mostrar detalle de un libro
# ----------------------
@router.get("/libros/{libro_id}", response_class=HTMLResponse)
async def detail_libro_html(request: Request, libro_id: str):
    try:
        libro_id_int = int(libro_id)
        if libro_id_int <= 0:
            raise ValueError
    except ValueError:
        print(f"[ERROR] ID no válido: {libro_id}")
        raise HTTPException(
            status_code=422,
            detail=f"El ID debe ser un número entero positivo. Se recibió: {libro_id}"
        )

    libro = db_libros.get_por_id(libro_id_int)
    if not libro:
        raise HTTPException(
            status_code=404,
            detail=f"Libro con ID {libro_id_int} no encontrado"
        )

    autores = db_autores.get_todos()
    editoriales = db_editoriales.get_todos()
    categorias = db_categorias.get_todos()
    ubicaciones = db_ubicaciones.get_todos()

    return templates.TemplateResponse(
        "libros/detail.html",
        {
            "request": request,
            "libro": libro,
            "libro_id": libro_id_int,
            "autores": autores,
            "editoriales": editoriales,
            "categorias": categorias,
            "ubicaciones": ubicaciones
        }
    )


@router.post("/libros/{libro_id}/eliminar")
def eliminar_libro(libro_id: int):
    try:
        libro = db_libros.eliminar(libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
    except ValueError as e:
        # Si el core lanza ValueError (libro con préstamos)
        return RedirectResponse(
            url=f"/libros?error={str(e)}",
            status_code=303
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return RedirectResponse(url="/libros", status_code=303)
