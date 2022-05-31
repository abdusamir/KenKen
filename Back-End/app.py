from flask import Flask,request,jsonify,session
from kenken import get_kenken
from datetime import timedelta
from flask_cors import CORS
app = Flask(__name__)

CORS(app,resources={r"/*": {"origins": "*"}})
app.secret_key = "super secret key"

@app.before_request
def make_session_permenant():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def index():
    return "<h1>Welcome to kenken api</h1>"

@app.route('/kenken', methods=['POST','GET'])
def kenken_game():
    if request.method == 'POST':
        json_req=request.json
        size=int(json_req['size'])
        algorithm=int(json_req['algorithm'])
        result=get_kenken(size=size,algorithm=algorithm)
        result=jsonify(result)
        return result
    else:
        return '<h1>You should use POST request :)</h1>'
if __name__ == '__main__':
    app.run()