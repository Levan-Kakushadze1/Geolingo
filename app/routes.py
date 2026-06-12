from flask import Blueprint, render_template

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/')
def home():
    from app.models import Lesson
    lessons = Lesson.query.all()
    return render_template('home.html', lessons=lessons)

@lessons_bp.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    from app.models import Lesson
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson.html', lesson=lesson)