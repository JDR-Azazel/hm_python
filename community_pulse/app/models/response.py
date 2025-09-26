from app.models.questions import Category, Question
from app.models import db

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.String(255), nullable=False)

    question = db.relationship('Question', back_populates='responses')

    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'is_agree': self.is_agree,
            'text': self.text
        }
