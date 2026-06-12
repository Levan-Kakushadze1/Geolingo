from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    return app

app = create_app()

from app.routes import lessons_bp
app.register_blueprint(lessons_bp)

if __name__ == '__main__':
    app.run(debug=True)