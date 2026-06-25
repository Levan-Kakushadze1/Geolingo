from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from app.models import Lesson
from app.extensions import db

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/')
def home():
    if current_user.is_authenticated:
        lessons = Lesson.query.all()
        completed_ids = []
        from app.models import Progress
        completed = Progress.query.filter_by(
            user_id=current_user.id,
            completed=True
        ).all()
        completed_ids = [p.lesson_id for p in completed]
        return render_template('home.html', lessons=lessons, completed_ids=completed_ids)
    return render_template('landing.html')

@lessons_bp.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    if not lesson.content:
        from app.ai_generator import generate_lesson_content
        lesson.content = generate_lesson_content(lesson.title)
        db.session.commit()

    return render_template('lesson.html', lesson=lesson)

@lessons_bp.route('/admin/edit/<int:lesson_id>', methods=['GET', 'POST'])
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    if request.method == 'POST':
        lesson.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('lessons.lesson', lesson_id=lesson_id))

    return render_template('edit_lesson.html', lesson=lesson)

@lessons_bp.route('/profile')
@login_required
def profile():
    total_lessons = Lesson.query.count()
    return render_template('profile.html', total_lessons=total_lessons)

@lessons_bp.route('/leaderboard')
def leaderboard():
    from app.models import User
    users = User.query.order_by(User.xp.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)

@lessons_bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        from app.ai_generator import chat_with_georgian_teacher
        user_message = request.form.get('message')
        session['chat_history'].append({"role": "user", "content": user_message})

        response = chat_with_georgian_teacher(session['chat_history'])
        session['chat_history'].append({"role": "assistant", "content": response})
        session.modified = True

    return render_template('chat.html', history=session.get('chat_history', []))

@lessons_bp.route('/chat/clear')
@login_required
def clear_chat():
    session.pop('chat_history', None)
    return redirect(url_for('lessons.chat'))