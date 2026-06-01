# NoticeBoard

Tablero de anuncios colaborativo desarrollado con Python y Flask.  
Permite publicar, consultar y eliminar anuncios clasificados por categoría.

## Requisitos

- Python 3.11 o superior
- pip

## Ejecución local (modo desarrollo)

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd noticeboard
```

### 2. Crear un entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python run.py
```

---

## Variables de entorno

Todas las configuraciones se pueden ajustar mediante variables de entorno, sin modificar el código fuente.

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `SECRET_KEY` | Clave secreta para sesiones Flask | `dev-secret-key-insegura` |
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///noticeboard.db` |
| `PORT` | Puerto en el que escucha la aplicación | `5000` |
| `FLASK_DEBUG` | Activa el modo debug (`1` = activo) | `0` |

Ejemplo de uso:

```bash
PORT=8080 FLASK_DEBUG=1 python run.py
```

---

## Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Lista todos los anuncios |
| GET | `/?category=Urgente` | Filtra anuncios por categoría |
| GET | `/new` | Formulario para crear un anuncio |
| POST | `/new` | Guarda un nuevo anuncio |
| GET | `/notice/<id>` | Detalle de un anuncio |
| POST | `/notice/<id>/delete` | Elimina un anuncio |
| GET | `/health` | Estado de la aplicación (JSON) |

---

## Estructura del proyecto

```
noticeboard/
├── app/
│   ├── __init__.py       # Factory de la aplicación Flask
│   ├── routes.py         # Rutas y controladores
│   ├── models.py         # Modelos de base de datos
│   ├── static/
│   │   └── style.css     # Estilos de la interfaz
│   └── templates/
│       ├── base.html     # Plantilla base
│       ├── index.html    # Lista de anuncios
│       ├── new.html      # Formulario de creación
│       └── notice.html   # Detalle de un anuncio
├── config.py             # Configuración centralizada
├── run.py                # Punto de entrada
├── requirements.txt      # Dependencias Python
└── README.md
```

---

## Categorías disponibles

- **General** — Anuncios de uso general
- **Urgente** — Comunicados que requieren atención inmediata
- **Académico** — Información relacionada con actividades académicas
- **Administrativo** — Avisos del área administrativa

---

## Notas para la práctica

Esta aplicación está diseñada para ser empaquetada en una imagen Docker.  
El repositorio **no incluye Dockerfile ni .dockerignore** — esos archivos son parte del trabajo a desarrollar.
