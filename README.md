# 📚 Proyecto Final - Gestión de Biblioteca

## 👨‍💻 Autor
**Sebastián Medina** – Diplomatura en Python

---

## 🎯 Descripción

Aplicación web desarrollada en **Python + FastAPI + SQLAlchemy + Jinja2** para la gestión de una biblioteca.  
Permite administrar **autores, libros, usuarios y préstamos**, aplicando reglas de negocio reales y control de stock.  

Se me entregaron únicamente los archivos relacionados con **autores** y **nacionalidades**.  
Tuve que **crear todos los modelos y schemas restantes** (libros, usuarios, préstamos, categorías, editoriales, roles, sanciones, reservas, eventos, ubicaciones, estados) debido a las **relaciones que existen entre las tablas**.

En cambio, en **core, api y frontend** implementé únicamente los endpoints y lógica necesarios para:  
- Autores  
- Libros  
- Usuarios  
- Préstamos  
- Wikipedia (API externa): permite mostrar un botón en la vista de autores que lleva a la página Wikipedia del autor, y en libros al resumen del libro.

---

## 🚀 Funcionalidades Implementadas

- ✅ **CRUD Autores**
- ✅ **CRUD Libros**
- ✅ **CRUD Usuarios**
- ✅ **CRUD Préstamos**

### 🔒 Reglas de negocio aplicadas
- ❌ No se pueden borrar **usuarios** con prestamos o historial de préstamos.  
- ❌ No se pueden borrar **libros** con préstamos asociados o historial de prestamos.  
- ❌ No se pueden borrar **autores** que tengan libros registrados, prestamos activos o historial de prestamos.  
- 🚫 No se permite prestar libros a **usuarios suspendidos o inactivos**.  
- ⏰ Se aplican **multas** si los usuarios entregan tarde o pierden un libro:
  - Al entregar tarde, se cobra una multa proporcional y el stock se **incrementa**.  
  - Si se pierde un libro, **no se renueva el stock** y se cobra la **multa máxima**.  
- 📉 Al generar un préstamo se **reduce el stock** de libros.  
- 📈 Al registrar una devolución se **incrementa el stock** de libros (excepto si se perdió).  
- 🌐 **Wikipedia:** botón en autores y libros que redirige a la página correspondiente para mostrar información adicional.


---

## 🗄️ Tablas del Proyecto

- **Entregadas en la consigna:**  
  - `autores`  
  - `nacionalidades`  

- **Creadas por mí (por las relaciones entre tablas):**  
  - `libros`  
  - `usuarios`  
  - `prestamos`  
  - `categorias`  
  - `editoriales`  
  - `roles`  
  - `sanciones`  
  - `reservas`  
  - `eventos`  
  - `ubicaciones`  
  - `estado`


---


## 🛠️ Tecnologías Utilizadas

- **Python 3.11**  
- **FastAPI** → backend y API REST  
- **SQLAlchemy** → ORM para la base de datos  
- **Pydantic** → validación de datos  
- **SQLite** → base de datos por defecto  
- **Jinja2** → templates HTML  
- **Bootstrap 5** → estilos y maquetado  

---

## ⚙️ Instalación y Ejecución

Sigue estos pasos para levantar la aplicación localmente:

### 1. Clonar el repositorio

git clone https://github.com/usuario/diplomatura-python-bases.git
cd diplomatura-python-bases

2. Crear y activar un entorno virtual

Linux / Mac:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias
pip install -r requirements.txt

4. Configurar variables de entorno

Copiar example.env a .env:
cp example.env .env    # Linux/Mac
copy example.env .env  # Windows
Editar .env según sea necesario (por ejemplo, configuración de base de datos).

5. Ejecutar la aplicación
uvicorn main:app --reload

6. Acceder a la aplicación
Frontend web: http://127.0.0.1:8000
Documentación API (Swagger UI): http://127.0.0.1:8000/docs
Documentación API (ReDoc): http://127.0.0.1:8000/redoc

---
```plaintext
📂 Estructura del Proyecto

📂 Proyecto
├── app/
│   ├── api/        # Endpoints backend (autores, libros, usuarios, préstamos, Wikipedia)
│   ├── core/       # Lógica de negocio (autores, libros, usuarios, préstamos)
│   ├── frontend/   # Endpoints frontend (HTML + Jinja2) para autores, libros, usuarios, préstamos
│   ├── models/     # Modelos SQLAlchemy (todas las tablas creadas)
│   └── schemas/    # Validación con Pydantic (todas las tablas creadas)
├── templates/      # Templates generales (base.html, navbar.html, etc.)
├── static/         # Archivos estáticos generales
├── instance/       # Instancia de la base de datos
├── docs/           # Documentación adicional o imágenes (por ejemplo DER)
├── .gitignore      # Archivos ignorados por Git
├── example.env     # Plantilla variables entorno
├── LICENSE         # Licencia del proyecto
├── main.py         # Punto de entrada aplicación
├── README.md       # Documentación principal
└── requirements.txt # Dependencias Python



## 🔄 Flujo del Código (Diagrama Visual)


            ┌────────────────────┐
            │    Frontend (HTML) │
            │  app/frontend/*.py │
            └─────────┬──────────┘
                      │ Peticiones / Formularios
                      ▼
            ┌────────────────────┐
            │       Core         │
            │  app/core/*.py     │
            │ CRUD + Validaciones│
            │ Reglas de negocio  │
            └───────┬────────────┘
                     │ Llama a
                     ▼
        ┌─────────────────────────┐
        │      Models             │
        │  app/models/*.py        │
        │ Define tablas y relaciones
        └─────────┬──────────────┘
                  │ Usa para validar/serializar
                  ▼
        ┌─────────────────────────┐
        │      Schemas            │
        │  app/schemas/*.py       │
        │ Validación Pydantic     │
        └─────────┬──────────────┘
                  │ Interactúa
                  ▼
        ┌─────────────────────────┐
        │   Base de Datos         │
        │ SQLite / PostgreSQL     │
        └─────────┬──────────────┘
                  │ Puede exponer datos
                  ▼
            ┌───────────────┐
            │ API REST      │
            │ app/api/*.py  │
            │ JSON endpoints│
            └───────────────┘
                      │ Consulta externa
                      ▼
            ┌────────────────────┐
            │ Wikipedia API      │
            │ URLs de autores o  │
            │ resúmenes de libros│
            └────────────────────┘
```
## 💡 Nota del Desarrollo

Durante el desarrollo de este proyecto, se utilizó **ChatGPT** para:

- Consultas sobre la estructura del código.  
- Reestructuración y optimización de lógicas de negocio.  
- Edición rapida y sugerencias de código en Python y SQL.  

Gracias a estas consultas, se pudieron resolver de manera más rápida problemas complejos y mejorar la claridad del proyecto. 

📝 TO DO / Notas

📄 Documentación: La documentación completa del proyecto no fue finalizada, aunque la API cuenta con documentación automática en Swagger disponible en http://127.0.0.1:8000/docs
.

🆔 ID de préstamos: Tras varias pruebas, el ID de la tabla prestamos se desincronizó y actualmente arranca desde 65.


💾 Backup de la base de datos: No se eliminó un archivo de backup (library.db) que quedó en la carpeta del proyecto; conviene eliminarlo antes de un commit final.

