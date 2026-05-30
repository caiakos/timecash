from flask import Blueprint, render_template, redirect, url_for, flash, abort, current_app
from datetime import date
from flask_login import login_required, current_user
from app import db
from app.models import Event
from app.events.forms import EventForm

events_bp = Blueprint('events', __name__)


@events_bp.route('/')
@login_required
def index():
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.date.asc()).all()
    return render_template('events/index.html', events=events, hoje=date.today())


@events_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            time=form.time.data,
            category=form.category.data,
            location=form.location.data,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Evento criado com sucesso!', 'success')
        current_app.logger.info(f'Evento criado: {event.title} por {current_user.email}')
        return redirect(url_for('events.index'))
    return render_template('events/form.html', form=form, title='Novo Evento')


@events_bp.route('/<int:event_id>/editar', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.time = form.time.data
        event.category = form.category.data
        event.location = form.location.data
        db.session.commit()
        flash('Evento atualizado!', 'success')
        return redirect(url_for('events.index'))
    return render_template('events/form.html', form=form, title='Editar Evento', event=event)


@events_bp.route('/<int:event_id>/excluir', methods=['POST'])
@login_required
def delete(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Evento excluído.', 'info')
    return redirect(url_for('events.index'))
