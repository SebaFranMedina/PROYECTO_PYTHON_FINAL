from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.core.database import get_db
from app.models.usuarios import Usuario as UsuarioModel
from app.models.prestamos import Prestamo  # Importar modelo de préstamos
from app.schemas.usuarios import Usuario, UsuarioBase

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# ----------------------
# Listar todos los usuarios
# ----------------------
@router.get("/", response_model=list[Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioModel).all()
    return usuarios

# ----------------------
# Obtener un usuario por ID
# ----------------------
@router.get("/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# ----------------------
# Crear usuario desde formulario HTML
# ----------------------
@router.post("/", response_model=None)
def crear_usuario_form(
    dni: str = Form(None),
    nombre: str = Form(None),
    apellido: str = Form(None),
    email: str = Form(None),
    rol_id: int = Form(None),
    estado_usuario_id: int = Form(None),
    usuario: UsuarioBase = None,
    db: Session = Depends(get_db)
):
    if usuario:
        nuevo_usuario = UsuarioModel(**usuario.dict())
    else:
        nuevo_usuario = UsuarioModel(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            email=email,
            rol_id=rol_id,
            estado_id=estado_usuario_id
        )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return RedirectResponse(url="/usuarios", status_code=303)

# ----------------------
# Editar usuario desde formulario HTML
# ----------------------
@router.post("/{usuario_id}/update", response_model=None)
def actualizar_usuario_form(
    usuario_id: int,
    dni: str = Form(None),
    nombre: str = Form(None),
    apellido: str = Form(None),
    email: str = Form(None),
    rol_id: int = Form(None),
    estado_usuario_id: str = Form(None),  # viene como string desde el form
    db: Session = Depends(get_db)
):
    usuario_db = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if dni is not None: usuario_db.dni = dni
    if nombre is not None: usuario_db.nombre = nombre
    if apellido is not None: usuario_db.apellido = apellido
    if email is not None: usuario_db.email = email
    if rol_id is not None: usuario_db.rol_id = rol_id

    # Convertir estado_usuario_id a int si viene
    if estado_usuario_id:
        try:
            usuario_db.estado_id = int(estado_usuario_id)
        except ValueError:
            raise HTTPException(status_code=422, detail="ID de estado inválido")

    db.commit()
    db.refresh(usuario_db)
    return RedirectResponse(url="/usuarios", status_code=303)


# ----------------------
# Eliminar usuario desde formulario HTML (con control de préstamos activos)
# ----------------------
@router.post("/{usuario_id}/eliminar", response_model=None)
def eliminar_usuario_form(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    if not usuario_db:
        return RedirectResponse(url="/usuarios?mensaje=Usuario+no+encontrado", status_code=303)
    
    # Verificar si tiene préstamos activos o cualquier préstamo
    prestamos = db.query(Prestamo).filter(Prestamo.usuario_id == usuario_id).count()
    
    if prestamos > 0:
        return RedirectResponse(
            url="/usuarios?mensaje=No+se+puede+eliminar,+el+usuario+tiene+préstamos",
            status_code=303
        )
    
    # No tiene préstamos, se elimina
    db.delete(usuario_db)
    db.commit()
    return RedirectResponse(url="/usuarios?mensaje=Usuario+eliminado+correctamente", status_code=303)


# ----------------------
# API JSON: Actualizar usuario
# ----------------------
@router.put("/{usuario_id}", response_model=Usuario)
def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioBase,
    db: Session = Depends(get_db)
):
    usuario_db = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in usuario.dict().items():
        setattr(usuario_db, key, value)
    
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

# ----------------------
# API JSON: Eliminar usuario
# ----------------------
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario_db)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}
