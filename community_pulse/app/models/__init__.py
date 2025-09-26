from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# импорт моделей для миграций и удобства
from app.models.response import Response
from app.models.questions import Question, Statistic