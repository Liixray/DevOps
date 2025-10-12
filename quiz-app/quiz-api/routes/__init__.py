from .questions import questions_bp
from .participations import participations_bp
from .quiz_info import quiz_info_bp

def register_blueprints(app):
    app.register_blueprint(questions_bp)
    app.register_blueprint(participations_bp)
    app.register_blueprint(quiz_info_bp)
