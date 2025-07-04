from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from app.middleware import auth, guest
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user


auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/login', methods=["GET","POST"])
@guest
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login Successfully','success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid username or password','danger')
    return render_template('login.html')


@auth_bp.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not email or not password or not confirm:
            flash('All fields are required!','danger')
        elif password != confirm:
            flash("Passwords do not match!", "danger")
        elif User.query.filter_by(email=email).first():
            flash('Email already registered!','warning')
        else:
            hashed_password = generate_password_hash(password)
            user = User(name=name, email=email, password=hashed_password) 
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully. Please login.','success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')



@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flash('User Logout Successfully','info')
    return redirect(url_for('auth.login'))