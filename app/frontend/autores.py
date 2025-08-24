from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from starlette.status import HTTP_303_SEE_OTHER

from app.core.database import get_db
from app.models.autores import Autor
from app.core.autores import db_autores
from app.core.nacionalidades import db_nacionalidades
from app.models.nacionalidades import Nacionalidad

router = APIRouter(tags=["Frontend Autores"])

# 📌 Templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# ----------------------
# Listar todos los autores
# ----------------------
@router.get("/autores", response_class=HTMLResponse)
async def list_autores(request: Request):
    autores = db_autores.get_todos()
    return templates.TemplateResponse(
        "autores/list.html",
        {"request": request, "autores": autores}
    )

# ----------------------
# Formulario de creación
# ----------------------
@router.get("/autores/create", response_class=HTMLResponse)
async def mostrar_formulario_creacion(request: Request):
    nacionalidades = db_nacionalidades.get_todos(order_by=Nacionalidad.sdes)
    return templates.TemplateResponse(
        "autores/create.html",
        {"request": request, "nacionalidades": nacionalidades}
    )

# ----------------------
# Crear nuevo autor
# ----------------------
@router.post("/autores/create")
async def crear_autor(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    fecha_nacimiento: str = Form(None),
    nacionalidad_id: int = Form(...),
    biografia: str = Form(None),
    db: Session = Depends(get_db)
):
    # Convertir string a date
    fecha_nacimiento_date = None
    if fecha_nacimiento:
        try:
            fecha_nacimiento_date = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        except ValueError:
            return templates.TemplateResponse(
                "autores/create.html",
                {
                    "request": request,
                    "nacionalidades": db_nacionalidades.get_todos(order_by=Nacionalidad.sdes),
                    "error": "Fecha de nacimiento inválida, usar formato YYYY-MM-DD",
                    "valores": {
                        "nombre": nombre,
                        "apellido": apellido,
                        "fecha_nacimiento": fecha_nacimiento,
                        "nacionalidad_id": nacionalidad_id,
                        "biografia": biografia
                    }
                }
            )

    nuevo_autor = Autor(
        nombre=nombre,
        apellido=apellido,
        fecha_nacimiento=fecha_nacimiento_date,
        nacionalidad_id=nacionalidad_id,
        biografia=biografia
    )
    db.add(nuevo_autor)
    db.commit()
    return RedirectResponse(url="/autores", status_code=303)

# ----------------------
# Detalle de autor
# ----------------------
@router.get("/autores/{autor_id}", response_class=HTMLResponse)
async def detail_autor_html(request: Request, autor_id: int):
    autor = db_autores.get_por_id(autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    nacionalidades = db_nacionalidades.get_todos(order_by=Nacionalidad.sdes)
    return templates.TemplateResponse(
        "autores/detail.html",
        {"request": request, "autor": autor, "nacionalidades": nacionalidades}
    )

@router.post("/autores/{autor_id}/eliminar")
def eliminar_autor(autor_id: int):
    try:
        autor = db_autores.eliminar(autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
    except ValueError as e:
        return RedirectResponse(
            url=f"/autores?error={str(e)}",
            status_code=303
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return RedirectResponse(url="/autores", status_code=303)
