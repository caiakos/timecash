from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    name = StringField('Nome completo', validators=[DataRequired(message='Nome obrigatório'), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(message='Email obrigatório'), Email(message='Email inválido')])
    password = PasswordField('Senha', validators=[DataRequired(message='Senha obrigatória'), Length(min=6, message='Mínimo 6 caracteres')])
    confirm = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password', message='Senhas não conferem')])
    submit = SubmitField('Cadastrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Este email já está cadastrado.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Email obrigatório'), Email(message='Email inválido')])
    password = PasswordField('Senha', validators=[DataRequired(message='Senha obrigatória')])
    submit = SubmitField('Entrar')
