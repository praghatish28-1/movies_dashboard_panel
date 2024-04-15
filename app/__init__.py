# app/__init__.py
from flask import Flask
from .celery_config import make_celery, celery
from flask_pymongo import PyMongo
import app.db as db
from app.utils.logging_config import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.mongo = PyMongo(app)
    setup_logging()

    # Properly configure and assign Celery
    global celery
    celery = make_celery(app)

    from .views import auth_views, csv_views, bp
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(csv_views.bp)
    app.register_blueprint(bp)

    return app, celery
