from flask import Flask, make_response, request
from db import init_db, Base, engine
from routes import register_blueprints
from flask_cors import CORS
from jwt_utils import decode_token, JwtError


port = 8282
app = Flask(__name__)
application = app
CORS(app, resources={r"/*": {"origins": "*"}})

init_db()
register_blueprints(app)

@app.route('/', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    origin = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'


@app.route('/validate-token/', methods=['GET'])
def validate_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return {"error": "Unauthorized"}, 401

    token = auth_header.split('Bearer ')[1]
    try:
        sub = decode_token(token)
        if sub == "quiz-app-admin":
            return {"message": "Token is valid"}, 200
        return {"error": "Unauthorized"}, 401
    except JwtError as e:
        return {"error": str(e)}, 401


@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return {"error": "Unauthorized"}, 401

    token = auth_header.split('Bearer ')[1]
    try:
        sub = decode_token(token)
        if sub != "quiz-app-admin":
            return {"error": "Unauthorized"}, 401
    except JwtError as e:
        return {"error": str(e)}, 401

    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        return {"message": "Database has been reset successfully."}, 200
    except Exception as e:
        return {"error": f"Failed to reset database: {str(e)}"}, 500


if __name__ == "__main__":
    app.run(debug=True)
