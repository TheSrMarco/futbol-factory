import os
from urllib.parse import quote_plus  # <--- ESTO ARREGLA EL ERROR UNICODE

class Config:
    # --- EDITA TUS DATOS AQUÍ ---
    DB_USER = "postgres"
    DB_PASS = "123"  # Pon tu contraseña real (aunque tenga tildes)
    DB_HOST = "localhost"
    DB_NAME = "ffactory"        # El nombre de tu base de datos
    # ----------------------------

    # Codificamos los datos para que PostgreSQL no se queje por caracteres raros
    _user = quote_plus(DB_USER)
    _pass = quote_plus(DB_PASS)
    _name = quote_plus(DB_NAME)

    # Armamos la URL final automáticamente
    SQLALCHEMY_DATABASE_URI = f"postgresql://{_user}:{_pass}@{DB_HOST}:5432/{_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False