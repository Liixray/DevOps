from flask import Flask, make_response, request
from db import init_db
from routes import register_blueprints
from flask_cors import CORS


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

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

if __name__ == "__main__":
    app.run(debug=True)
