# 📚 Proyecto Final - Gestión de Biblioteca

## 👨‍💻 Autor
**Sebastián Medina** – Diplomatura en Python (Bases de Datos y FastAPI)

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
- ❌ No se pueden borrar **usuarios** con historial de préstamos.  
- ❌ No se pueden borrar **libros** con préstamos asociados.  
- ❌ No se pueden borrar **autores** que tengan libros registrados.  
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

- **No implementadas:**  
  - `configuracion`  
  - `sql_sequence`  

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

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/diplomatura-python-bases
   cd diplomatura-python-bases
Crear y activar un entorno virtual:


python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Instalar dependencias:


pip install -r requirements.txt
Configurar variables de entorno:

Copiar example.env a .env y ajustar según sea necesario.

Ejecutar la aplicación:
uvicorn main:app --reload

👉 La aplicación estará disponible en: http://127.0.0.1:8000

📂 Estructura del Proyecto

app/
├── api/           # Endpoints backend (autores, libros, usuarios, préstamos, Wikipedia)
├── core/          # Lógica de negocio (autores, libros, usuarios, préstamos)
├── frontend/      # Endpoints frontend (HTML + Jinja2) para autores, libros, usuarios, préstamos
├── models/        # Modelos SQLAlchemy (todas las tablas creadas)
├── schemas/       # Validación con Pydantic (todas las tablas creadas)
├── templates/     # Vistas HTML
├── static/        # Archivos estáticos (CSS/JS)
├── .gitignore                # Archivos ignorados por Git
├── example.env               # Plantilla variables entorno
├── LICENSE                   # Licencia del proyecto
├── main.py                   # Punto entrada aplicación
├── README.md                 # Documentación principal
└── requirements.txt          # Dependencias Python
└── library.db                # Backup DB olvidado

## 🔄 Flujo del Código (Diagrama Visual)

```plaintext
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
## 💡 Nota del Desarrollo

Durante el desarrollo de este proyecto, se utilizó **ChatGPT** para:

- Consultas sobre la estructura del código.  
- Reestructuración y optimización de lógicas de negocio.  
- Edición y sugerencias de código en Python y SQL.  

Gracias a estas consultas, se pudieron resolver de manera más rápida problemas complejos y mejorar la claridad del proyecto. 

TO DO / Notas

No se completó la documentación del proyecto.

En la pestaña de préstamos, tras varias pruebas el ID de préstamos se corría y actualmente arranca en 65.

Tablas configuracion y sql_sequence no fueron implementadas porque no eran necesarias para la funcionalidad entregada.

No se pudo borrar un backup de la base de datos copiada en la carpeta del proyecto

