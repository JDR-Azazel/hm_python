from flask import Flask
from config import DevelopmentConfig
from app.models import db
from app.routers.questions import questions_bp
from app.routers.response import response_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    # Чиним отображение кириллицы в JSON
    app.config['JSON_AS_ASCII'] = False

    from flask_migrate import Migrate
    migrate = Migrate()
    migrate.init_app(app, db)

    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)
    return app
