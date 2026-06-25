from run import app
from app.extensions import db
from app.models import Lesson

with app.app_context():
    lessons = [
        Lesson(title="The Georgian Alphabet", description="Learn the unique Georgian script", order=1),
        Lesson(title="Basic Greetings", description="Say hello and goodbye in Georgian", order=2),
        Lesson(title="Numbers 1-10", description="Count from one to ten in Georgian", order=3),
        Lesson(title="Colors", description="Learn color words in Georgian", order=4),
        Lesson(title="Family Members", description="Words for family in Georgian", order=5),
        Lesson(title="Days of the Week", description="Learn the days in Georgian", order=6),
        Lesson(title="Food and Drinks", description="Common food vocabulary in Georgian", order=7),
        Lesson(title="Common Phrases", description="Useful everyday phrases in Georgian", order=8),
    ]

    db.session.add_all(lessons)
    db.session.commit()
    print("Lessons created successfully!")