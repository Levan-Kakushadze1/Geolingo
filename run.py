from flask import Flask
from config import Config
from app.extensions import db, login_manager, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    return app

app = create_app()

from app.routes import lessons_bp
from app.auth import auth_bp
from app.quiz import quiz_bp
app.register_blueprint(lessons_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)


if __name__ == '__main__':
    app.run(debug=True)