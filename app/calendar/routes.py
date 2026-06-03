from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Event, Finance
from datetime import date, datetime
import calendar as cal

calendar_bp = Blueprint('calendar', __name__)


@calendar_bp.route('/')
@login_required
def index():
    hoje = date.today()
    mes = int(request.args.get('mes', hoje.month))
    ano = int(request.args.get('ano', hoje.year))

    if mes < 1:
        mes = 12
        ano -= 1
    elif mes > 12:
        mes = 1
        ano += 1

    events = Event.query.filter_by(user_id=current_user.id).filter(
        Event.date >= date(ano, mes, 1),
        Event.date <= date(ano, mes, cal.monthrange(ano, mes)[1])
    ).all()

    events_by_day = {}
    for e in events:
        event_date = e.date
        if isinstance(event_date, str):
            event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
        elif hasattr(event_date, 'date'):
            event_date = event_date.date()
        day = event_date.day
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(e)

    month_calendar = cal.monthcalendar(ano, mes)
    month_name = cal.month_name[mes]

    finances = Finance.query.filter_by(user_id=current_user.id).filter(
        Finance.date >= date(ano, mes, 1),
        Finance.date <= date(ano, mes, cal.monthrange(ano, mes)[1])
    ).all()
    total_entradas = sum(f.amount for f in finances if f.type == 'entrada')
    total_saidas = sum(f.amount for f in finances if f.type == 'saida')

    try:
        total_futuros = sum(
            f.amount for f in finances
            if f.type == 'saida' and (
                f.date.date() if hasattr(f.date, 'date') else f.date
            ) > hoje
        )
    except Exception:
        total_futuros = 0.0

    return render_template('calendar/index.html',
                           month_calendar=month_calendar,
                           events_by_day=events_by_day,
                           month_name=month_name,
                           mes=mes, ano=ano,
                           total_entradas=total_entradas,
                           total_saidas=total_saidas,
                           total_futuros=total_futuros,
                           hoje=hoje)
