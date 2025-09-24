from .questions import questions_bp

def register_blueprints(app):
    app.register_blueprint(questions_bp)
