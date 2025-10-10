from .questions import questions_bp
from .auth import auth_bp
from .auth_user import auth_user_bp 

def register_blueprints(app):
    app.register_blueprint(questions_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(auth_user_bp)
