from flask import Blueprint, render_template, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Finance, Event
from app.finances.forms import FinanceForm
from datetime import date

finances_bp = Blueprint('finances', __name__)


@finances_bp.route('/')
@login_required
def index():
    finances = Finance.query.filter_by(user_id=current_user.id).order_by(Finance.date.desc()).all()
    hoje = date.today()
    total_entradas = sum(f.amount for f in finances if f.type == 'entrada' and f.date.month == hoje.month and f.date.year == hoje.year)
    total_saidas = sum(f.amount for f in finances if f.type == 'saida' and f.date.month == hoje.month and f.date.year == hoje.year)
    saldo = total_entradas - total_saidas
    futuros = sum(f.amount for f in finances if f.type == 'saida' and f.date > hoje)
    return render_template('finances/index.html',
                           finances=finances,
                           total_entradas=total_entradas,
                           total_saidas=total_saidas,
                           saldo=saldo,
                           futuros=futuros)


@finances_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def create():
    form = FinanceForm()
    events = Event.query.filter_by(user_id=current_user.id).all()
    form.set_event_choices(events)
    if form.validate_on_submit():
        event_id = form.event_id.data if form.event_id.data != 0 else None
        finance = Finance(
            description=form.description.data,
            amount=form.amount.data,
            type=form.type.data,
            date=form.date.data,
            event_id=event_id,
            user_id=current_user.id
        )
        db.session.add(finance)
        db.session.commit()
        flash('Transação adicionada!', 'success')
        current_app.logger.info(f'Finança criada: {finance.description} por {current_user.email}')
        return redirect(url_for('finances.index'))
    return render_template('finances/form.html', form=form, title='Nova Transação')


@finances_bp.route('/<int:finance_id>/excluir', methods=['POST'])
@login_required
def delete(finance_id):
    finance = Finance.query.get_or_404(finance_id)
    if finance.user_id != current_user.id:
        abort(403)
    db.session.delete(finance)
    db.session.commit()
    flash('Transação excluída.', 'info')
    return redirect(url_for('finances.index'))
