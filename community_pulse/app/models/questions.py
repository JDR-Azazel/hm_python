from app.models import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    # связь с вопросами
    questions = relationship('Question', back_populates='category')


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    responses = db.relationship('Response', back_populates='question', lazy=True)

    # внешний ключ на Category
    category_id = db.Column(db.Integer, ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='questions')


    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "category": self.category.name if self.category else None
        }


class Statistic(db.Model):
    __tablename__ = 'statistics'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'question_id': self.question_id,
            'agree_count': self.agree_count,
            'disagree_count': self.disagree_count
        }
