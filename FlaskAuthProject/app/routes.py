from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from .models import User
from app.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/')
def home():
    return render_template('home.html')

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('auth.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
