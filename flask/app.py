from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure key
jwt = JWTManager(app)
CORS(app)

users = {
    "testuser": {
        "password": "testpassword",
        "profile": {
            "name": "Test User",
            "email": "testuser@example.com"
        }
    }
}

@app.route('/')
def index():
    return render_template('home.html', title='Home')  # Ensure home.html exists in templates folder

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = users.get(username)

    if not user or user['password'] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user_profile = users[current_user]['profile']
    return jsonify(user_profile=user_profile)

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)

@app.route('/about')
def about():
    title = 'About us'
    return render_template("about.html", title=title)

if __name__ == '__main__':
    app.run(debug=True)
