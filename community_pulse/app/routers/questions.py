from flask import Blueprint, request, Response as FlaskResponse, jsonify
from app.models.questions import Question
from app.models.response import Response
from app.models import db
import json

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

def question_to_dict(q: Question):
    return {
        'id': q.id,
        'текст': q.text,
        'категория': q.category.name if q.category else None,
        'ответы': [
            {
                'id': r.id,
                'текст': r.text,
                'is_agree': r.is_agree
            } for r in q.responses
        ]
    }

@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    data = [question_to_dict(q) for q in questions]
    # Красивый, читаемый JSON
    return FlaskResponse(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    q = Question.query.get_or_404(id)
    return FlaskResponse(
        json.dumps(question_to_dict(q), ensure_ascii=False, indent=2),
        mimetype='application/json'
    )



@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json() or {}
    text = data.get('text')
    if not text:
        return jsonify({'error': 'text required'}), 400
    q = Question(text=text)
    db.session.add(q)
    db.session.commit()
    return jsonify(question_to_dict(q)), 201


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    q = Question.query.get_or_404(id)
    data = request.get_json() or {}
    q.text = data.get('text', q.text)
    db.session.commit()
    return jsonify(question_to_dict(q))


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    q = Question.query.get_or_404(id)
    db.session.delete(q)
    db.session.commit()
    return jsonify({'deleted': id})
