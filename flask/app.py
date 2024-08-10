from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # For session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataB.db'  # Path to your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB
db = SQLAlchemy(app)
CORS(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'  # Explicitly name the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    profile_picture = db.Column(db.String(120), default='default.jpg')

    def __repr__(self):
        return f'<User {self.username}>'


# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials!", 401

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if user:
        if request.method == 'POST':
            file = request.files.get('profile_picture')
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename
                db.session.commit()
                return redirect(url_for('profile'))

        return render_template('home.html', user=user.username, balance=user.balance, profile_picture=user.profile_picture)
    else:
        return "User not found", 404

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/about')
def about():
    title = 'About us'
    return render_template("about.html", title=title)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
