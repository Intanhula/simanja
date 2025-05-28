from flask import Blueprint, render_template, redirect, url_for, request, session
from simanja.models import user as user_model

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if username and password and email:
            success = user_model.create_user(username, password, email)
            if success:
                return redirect(url_for('auth.login'))
            else:
                message = "User atau email sudah terdaftar."
        else:
            message = "Username dan password harus diisi."
    return render_template('auth/register.html', message=message)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_model.verify_login(username, password):
            session['user'] = username
            return redirect(url_for('auth.dashboard'))
        else:
            message = "Gagal login, username atau password salah."
    return render_template('auth/login.html', message=message)

@auth_bp.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard/index.html', user=session['user'])

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))

