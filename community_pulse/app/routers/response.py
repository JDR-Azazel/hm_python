from flask import Blueprint, request, jsonify
from app.models.response import Response
from app.models.questions import Question, Statistic
from app.models import db


response_bp = Blueprint('responses', __name__, url_prefix='/responses')


@response_bp.route('/', methods=['GET'])
def get_responses():
    stats = Statistic.query.all()
    return jsonify([s.to_dict() for s in stats])


@response_bp.route('/', methods=['POST'])
def add_response():
    data = request.get_json() or {}
    question_id = data.get('question_id')
    is_agree = data.get('is_agree')
    if question_id is None or is_agree is None:
        return jsonify({'error': 'question_id and is_agree required'}), 400


    q = Question.query.get_or_404(question_id)
    r = Response(question_id=question_id, is_agree=bool(is_agree))
    db.session.add(r)


    # Обновляем статистику
    stat = Statistic.query.filter_by(question_id=question_id).first()
    if not stat:
        stat = Statistic(question_id=question_id, agree_count=0, disagree_count=0)
        db.session.add(stat)
    if r.is_agree:
        stat.agree_count += 1
    else:
        stat.disagree_count += 1


    db.session.commit()
    return jsonify({'ok': True}), 201