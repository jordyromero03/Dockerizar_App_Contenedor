import os

class Config:
    # Clave secreta para sesiones Flask — debe cambiarse en producción
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-insegura")

    # URL de la base de datos. Por defecto usa SQLite local.
    # En producción puede apuntarse a PostgreSQL u otro motor.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///noticeboard.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Puerto en el que escucha la aplicación
    PORT = int(os.environ.get("PORT", 5000))

    # Modo debug — nunca True en producción
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
