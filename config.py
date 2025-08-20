import os

from flask import Flask


class BaseConfig:
    BCRYPT_SALT = b"$2b$12$BuJdiyOo2JcUDFgYFhU6Lu"
    DEBUG = True
    DOMAIN = "robinhood.com"
    PICTURES_DIR = "./pictures"
    SECRET_KEY = "0000000000000000000000000000000000000000000="
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(BaseConfig):
    EMPLOYEE_API_URL = "http://localhost:8080/lookup/"


class ProductionConfig(BaseConfig):
    DEBUG = False
    EMPLOYEE_API_URL = "http://directory.nginx.service/lookup/"
    SECRET_KEY = "s337eH1wD9rb42dIb4QsfcTghAWLE5c2DIt3ROpVjv4="


config_map = {
    "default": BaseConfig,
    "local": LocalConfig,
    "test": LocalConfig,
    "production": ProductionConfig,
}


def configure(app: Flask):
    app.config.from_object(
        config_map.get(os.getenv("FLASK_ENV"), config_map["default"])
    )
    app.secret_key = app.config.get("SECRET_KEY")
