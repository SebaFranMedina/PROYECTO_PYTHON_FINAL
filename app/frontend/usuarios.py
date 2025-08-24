from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from starlette.status import HTTP_303_SEE_OTHER
from fastapi.templating import Jinja2Templates

from app.core.usuarios import db_usuarios
from app.core.roles import db_roles
from app.core.estados import db_estados



router = APIRouter(tags=["Frontend Usuarios"])

# 📌 Ruta absoluta a la carpeta de templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # sube hasta la raíz del proyecto
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ----------------------
# Listar todos los usuarios
# ----------------------
@router.get("/usuarios", response_class=HTMLResponse)
async def list_usuarios(request: Request):
    usuarios = db_usuarios.get_todos()
    return templates.TemplateResponse(
        "usuarios/list.html",
        {"request": request, "usuarios": usuarios}
    )


# ----------------------
# Mostrar formulario de creación de usuario
# ----------------------
@router.get("/usuarios/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    roles = sorted(db_roles.get_todos(), key=lambda r: r.nombre)
    estados = db_estados.get_todos(order_by="nombre")

    return templates.TemplateResponse(
        "usuarios/create.html",
        {
            "request": request,
            "roles": roles,
            "estados": estados,
            "valores": {}
        }
    )


# ----------------------
# Procesar creación de usuario (POST)
# ----------------------
@router.post("/usuarios/create")
async def crear_usuario(
    dni: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    rol_id: int = Form(...),
    estado_id: int = Form(...)
):
    nuevo_usuario = {
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "rol_id": rol_id,
        "estado_id": estado_id,
    }

    db_usuarios.crear(nuevo_usuario)
    return RedirectResponse(url="/usuarios", status_code=HTTP_303_SEE_OTHER)


# ----------------------
# Mostrar detalle de un usuario
# ----------------------
@router.get("/usuarios/{usuario_id}", response_class=HTMLResponse)
async def detail_usuario_html(request: Request, usuario_id: str):
    try:
        usuario_id_int = int(usuario_id)
        if usuario_id_int <= 0:
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"El ID debe ser un número entero positivo. Se recibió: {usuario_id}"
        )

    usuario = db_usuarios.get_por_id(usuario_id_int)
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {usuario_id_int} no encontrado"
        )

    # Obtener roles y estados para el detalle
    roles = sorted(db_roles.get_todos(), key=lambda r: r.nombre)
    estados = db_estados.get_todos(order_by="nombre")

    return templates.TemplateResponse(
        "usuarios/detail.html",
        {
            "request": request,
            "usuario": usuario,
            "usuario_id": usuario_id_int,
            "roles": roles,
            "estados": estados
        }
    )
