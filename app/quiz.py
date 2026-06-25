from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from app.ai_generator import generate_exercises
from app.extensions import db
from app.models import Lesson, Progress

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz/<int:lesson_id>')
@login_required
def quiz(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    exercises = generate_exercises(lesson.title, count=5)
    session['exercises'] = exercises
    session['lesson_id'] = lesson_id
    session['current'] = 0
    session['score'] = 0
    return redirect(url_for('quiz.question'))

@quiz_bp.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    exercises = session.get('exercises', [])
    current = session.get('current', 0)
    lesson_id = session.get('lesson_id')

    if current >= len(exercises):
        return redirect(url_for('quiz.result'))

    ex = exercises[current]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        is_correct = user_answer.strip() == ex['correct_answer'].strip()

        if is_correct:
            session['score'] = session.get('score', 0) + 1
            current_user.xp += 10
            db.session.commit()

        session['current'] = current + 1
        session['last_correct'] = is_correct
        session['last_answer'] = ex['correct_answer']
        return redirect(url_for('quiz.question'))

    return render_template('question.html', exercise=ex, current=current+1, total=len(exercises))

@quiz_bp.route('/result')
@login_required
def result():
    score = session.get('score', 0)
    total = len(session.get('exercises', []))
    lesson_id = session.get('lesson_id')

    progress = Progress.query.filter_by(
        user_id=current_user.id,
        lesson_id=lesson_id
    ).first()

    if progress:
        if score > progress.score:
            progress.score = score
        if score == total:
            progress.completed = True
    else:
        progress = Progress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            completed=(score == total),
            score=score
        )
        db.session.add(progress)

    db.session.commit()

    return render_template('result.html', score=score, total=total, lesson_id=lesson_id)