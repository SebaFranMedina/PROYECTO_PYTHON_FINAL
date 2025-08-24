from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

# -------------------
# Routers API
# -------------------
from app.api.autores import router as autores_router
from app.api.libros import router as libros_router
from app.api.usuarios import router as usuarios_router
from app.api.prestamos import router as prestamos_router
from app.api.wikipedia import router as wikipedia_router

# -------------------
# Routers Frontend
# -------------------
from app.frontend.autores import router as frontend_autores_router
from app.frontend.libros import router as frontend_libros_router
from app.frontend.usuarios import router as frontend_usuarios_router
from app.frontend.prestamos import router as frontend_prestamos_router
from app.frontend.wikipedia import router as frontend_wikipedia_router

# -------------------
# Crear app FastAPI
# -------------------
app = FastAPI(
    title="Open Biblioteca API",
    version="1.0.0",
    description="Sistema de gestión de biblioteca con API y Frontend"
)

# -------------------
# Archivos estáticos y templates
# -------------------
static_path = Path(__file__).parent / "static"
templates_path = Path(__file__).parent / "templates"

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

# -------------------
# Routers API (solo JSON)
# -------------------
app.include_router(autores_router, prefix="/api", tags=["Autores"])
app.include_router(libros_router, prefix="/api", tags=["Libros"])
app.include_router(usuarios_router, prefix="/api", tags=["Usuarios"])
app.include_router(prestamos_router, prefix="/api", tags=["Préstamos"])
app.include_router(wikipedia_router, prefix="/api", tags=["Wikipedia"])

# -------------------
# Routers Frontend (templates)
# -------------------
app.include_router(frontend_autores_router)
app.include_router(frontend_libros_router)
app.include_router(frontend_usuarios_router)
app.include_router(frontend_prestamos_router)  # ✅ aquí van tus /prestamos
app.include_router(frontend_wikipedia_router)

# -------------------
# Ruta raíz
# -------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# -------------------
# Ejecutar:
# uvicorn main:app --reload
# -------------------

