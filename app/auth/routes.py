from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('calendar.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            current_app.logger.info(f'Login: {user.email}')
            return redirect(url_for('calendar.index'))
        flash('Email ou senha incorretos.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('calendar.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Conta criada com sucesso! Faça login.', 'success')
        current_app.logger.info(f'Novo usuário: {user.email}')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    current_app.logger.info(f'Logout: {current_user.email}')
    logout_user()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('auth.login'))
