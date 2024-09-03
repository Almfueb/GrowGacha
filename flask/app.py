from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory, flash
from werkzeug.utils import secure_filename
import os

from models import db, User, History, MDMAccount, ANCIENTAccount, ELITEAccount
from function import move_account_to_history

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/profpic'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db.init_app(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('accounts'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

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
            return redirect(url_for('accounts'))
        else:
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        if 'profile_picture' in request.files:
            file = request.files.get('profile_picture')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename
                db.session.commit()
                flash('Profile picture updated successfully!', 'success')
                return redirect(url_for('accounts'))

    ancient_stock = ANCIENTAccount.query.count()
    elite_stock = ELITEAccount.query.count()
    mdma_stock = MDMAccount.query.count()

    return render_template(
        'home.html',
        user=user.username,
        balance=user.balance,
        profile_picture=user.profile_picture,
        ancient_stock=ancient_stock,
        elite_stock=elite_stock,
        mdma_stock=mdma_stock
    )

@app.route('/locks', methods=['GET', 'POST'])
def locks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        if 'profile_picture' in request.files:
            file = request.files.get('profile_picture')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename
                db.session.commit()
                flash('Profile picture updated successfully!', 'success')
                return redirect(url_for('locks'))

    return render_template('locks.html', user=user.username, balance=user.balance, profile_picture=user.profile_picture)

@app.route('/botting', methods=['GET', 'POST'])
def botting():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        if 'profile_picture' in request.files:
            file = request.files.get('profile_picture')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename
                db.session.commit()
                flash('Profile picture updated successfully!', 'success')
                return redirect(url_for('store'))

    return render_template('botting.html', user=user.username, balance=user.balance, profile_picture=user.profile_picture)

# New routes for locks1 and botting1
@app.route('/locks1', methods=['GET', 'POST'])
def locks1():
    return render_template('locks1.html')

@app.route('/botting1', methods=['GET', 'POST'])
def botting1():
    return render_template('botting1.html')


@app.route('/buyMDMA', methods=['POST'])
def buyMDMA():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in!'})

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'User not found!'})

    try:
        quantity = int(request.form.get('quantity', 0))
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid quantity!'})

    price_per_item = 50.00
    total_price = quantity * price_per_item

    if user.balance < total_price:
        return jsonify({'success': False, 'message': 'Insufficient balance!'})

    user.balance -= total_price
    db.session.commit()

    account = MDMAccount.query.order_by(MDMAccount.id).first()

    if account:
        move_account_to_history(account, user_id)
        
        session['purchased_account'] = {
            'username': account.username,
            'password': account.password,
            'rarity': account.rarity
        }

        return redirect(url_for('show'))
    else:
        return jsonify({'success': False, 'message': 'No account available.'})

@app.route('/buyElite', methods=['POST'])
def buyElite():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in!'})

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'User not found!'})

    quantity = int(request.form.get('quantity', 0))
    price_per_item = 7.50  # Replace with the actual price
    total_price = quantity * price_per_item

    if user.balance < total_price:
        return jsonify({'success': False, 'message': 'Insufficient balance!'})

    user.balance -= total_price
    db.session.commit()

    account = ELITEAccount.query.order_by(ELITEAccount.id).first()

    if account:
        move_account_to_history(account, user_id)
        
        session['purchased_account'] = {
            'username': account.username,
            'password': account.password,
            'rarity': account.rarity
        }

        return redirect(url_for('show'))
    else:
        return jsonify({'success': False, 'message': 'No account available.'})

@app.route('/buyAncient', methods=['POST'])
def buyAncient():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in!'})

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'User not found!'})

    quantity = int(request.form.get('quantity', 0))
    price_per_item = 5.00  # Replace with the actual price
    total_price = quantity * price_per_item

    if user.balance < total_price:
        return jsonify({'success': False, 'message': 'Insufficient balance!'})

    user.balance -= total_price
    db.session.commit()

    account = ANCIENTAccount.query.order_by(ANCIENTAccount.id).first()

    if account:
        move_account_to_history(account, user_id)
        
        session['purchased_account'] = {
            'username': account.username,
            'password': account.password,
            'rarity': account.rarity
        }

        return redirect(url_for('show'))
    else:
        return jsonify({'success': False, 'message': 'No account available.'})

@app.route('/editprofile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user and user.password == password:
            user.email = request.form['email']
            
            if 'profile_pic' in request.files:
                profile_pic = request.files['profile_pic']
                if profile_pic and profile_pic.filename != '':
                    filename = secure_filename(profile_pic.filename)
                    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    user.profile_picture = filename

            db.session.commit()
            flash('Your profile has been successfully updated!', 'success')
            return redirect(url_for('accounts'))
        else:
            flash('Username or password is incorrect. Please try again.', 'danger')
            return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/show')
def show():
    purchased_account = session.get('purchased_account')
    return render_template('show.html', account=purchased_account)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
