from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


CATEGORIES = [
    ('Geral', 'Geral'),
    ('Trabalho', 'Trabalho'),
    ('Saúde', 'Saúde'),
    ('Lazer', 'Lazer'),
    ('Compras', 'Compras'),
    ('Educação', 'Educação'),
    ('Família', 'Família'),
    ('Viagem', 'Viagem'),
]


class EventForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(message='Título obrigatório'), Length(max=150)])
    description = TextAreaField('Descrição', validators=[Optional(), Length(max=500)])
    date = DateField('Data', validators=[DataRequired(message='Data obrigatória')])
    time = TimeField('Horário', validators=[Optional()])
    category = SelectField('Categoria', choices=CATEGORIES, validators=[DataRequired()])
    location = StringField('Local', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Salvar')
