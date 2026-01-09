from flask import Blueprint
from flask import redirect, url_for, flash, request, render_template
from models import db, AppPost, User
from flask_login import current_user, login_required , login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

login_bp = Blueprint("login" , __name__)
register_bp = Blueprint("register" , __name__)
logout_bp = Blueprint("logout" , __name__)
profile_bp = Blueprint("profile" , __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home.index'))
        flash('Credenciais incorretas.', 'danger')
    return render_template('login.html')

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash('Este email já existe.', 'danger')
            return redirect(url_for('register.register'))
        hashed_pw = generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], email=request.form['email'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada! Podes fazer login.', 'success')
        return redirect(url_for('login.login'))
    return render_template('register.html')

@logout_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@profile_bp.route('/profile/update', methods=['POST'])
@login_required
def update_avatar():
    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower()
            if ext in ['png', 'jpg', 'jpeg', 'gif']:
                filename = f"avatar_{current_user.id}.{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.avatar = filename
                db.session.commit()
    return redirect(url_for('dashboard.dashboard'))