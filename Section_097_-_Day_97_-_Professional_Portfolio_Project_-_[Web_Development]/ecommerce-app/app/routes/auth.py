from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm
from app.models import User, Cart
from app.utils import generate_session_id

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            session_id = session.get('session_id')
            if session_id:
                Cart.merge_carts(user.id, session_id)
                session.pop('session_id', None)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.get_by_email(form.email.data):
            flash('Email already registered', 'error')
            return render_template('auth/register.html', form=form)
        user_id = User.create(form.email.data, form.password.data)
        if user_id:
            user = User.get(user_id)
            login_user(user)
            flash('Registration successful', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Registration failed', 'error')
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@auth_bp.before_app_request
def set_session_id():
    if not current_user.is_authenticated and 'session_id' not in session:
        session['session_id'] = generate_session_id()


@auth_bp.route('/profile')
@login_required
def profile():
    from app.models import Order
    orders = Order.get_by_user(current_user.id)
    return render_template('auth/profile.html', orders=orders)