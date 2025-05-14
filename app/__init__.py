import logging

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

log = logging.getLogger(__name__)
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure CORS
    allowed_origins = [origin.strip() for origin in Config.ALLOWED_ORIGINS.split(",")]
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    log.info(f"Using configuration: {config_class.__name__}")
    log.info(f"SQLALCHEMY_DATABASE_URI: {config_class.SQLALCHEMY_DATABASE_URI}")

    db.init_app(app)

    return app
