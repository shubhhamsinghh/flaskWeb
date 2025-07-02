from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from app.middleware import auth, guest

auth_bp = Blueprint('auth',__name__)

USER_CREDENTIALS = {
    'username' : 'admin',
    'password' : '123123'
}

@auth_bp.route('/login', methods=["GET","POST"])
@guest
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username
            flash('Login Successfully','success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid username or password','danger')
    return render_template('login.html')


@auth_bp.route('/logout')
@auth
def logout():
    session.pop('user', None)
    flash('User Logout Successfully','info')
    return redirect(url_for('auth.login'))