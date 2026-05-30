from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_login import current_user


class FinanceForm(FlaskForm):
    description = StringField('Descrição', validators=[DataRequired(message='Descrição obrigatória')])
    amount = FloatField('Valor (R$)', validators=[DataRequired(message='Valor obrigatório'), NumberRange(min=0.01, message='Valor deve ser maior que zero')])
    type = SelectField('Tipo', choices=[('entrada', 'Entrada'), ('saida', 'Saída')], validators=[DataRequired()])
    date = DateField('Data', validators=[DataRequired(message='Data obrigatória')])
    event_id = SelectField('Evento vinculado (opcional)', coerce=int, validators=[Optional()])
    submit = SubmitField('Salvar')

    def set_event_choices(self, events):
        self.event_id.choices = [(0, '-- Nenhum --')] + [(e.id, e.title) for e in events]
