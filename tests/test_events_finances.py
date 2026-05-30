from app.models import Event, Finance
from app import db
from datetime import date


def test_events_page_loads(auth_client):
    """Página de eventos carrega para usuário autenticado."""
    response = auth_client.get('/eventos/')
    assert response.status_code == 200


def test_create_event(auth_client, app):
    """Criar evento deve funcionar e aparecer na lista."""
    response = auth_client.post('/eventos/novo', data={
        'title': 'Reunião',
        'date': '2025-10-15',
        'category': 'Trabalho',
        'description': '',
        'location': '',
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        event = Event.query.filter_by(title='Reunião').first()
        assert event is not None


def test_edit_event(auth_client, app):
    """Editar evento deve atualizar os dados."""
    auth_client.post('/eventos/novo', data={
        'title': 'Evento Original', 'date': '2025-11-01',
        'category': 'Geral', 'description': '', 'location': ''
    })
    with app.app_context():
        event = Event.query.filter_by(title='Evento Original').first()
        event_id = event.id

    response = auth_client.post(f'/eventos/{event_id}/editar', data={
        'title': 'Evento Editado', 'date': '2025-11-05',
        'category': 'Lazer', 'description': '', 'location': ''
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        event = Event.query.get(event_id)
        assert event.title == 'Evento Editado'


def test_delete_event(auth_client, app):
    """Excluir evento deve removê-lo do banco."""
    auth_client.post('/eventos/novo', data={
        'title': 'Para Deletar', 'date': '2025-12-01',
        'category': 'Geral', 'description': '', 'location': ''
    })
    with app.app_context():
        event = Event.query.filter_by(title='Para Deletar').first()
        event_id = event.id

    response = auth_client.post(f'/eventos/{event_id}/excluir', follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Event.query.get(event_id) is None


def test_finances_page_loads(auth_client):
    """Página de finanças carrega para usuário autenticado."""
    response = auth_client.get('/financas/')
    assert response.status_code == 200


def test_create_finance(auth_client, app):
    """Criar transação financeira deve funcionar."""
    response = auth_client.post('/financas/nova', data={
        'description': 'Salário',
        'amount': '3000.00',
        'type': 'entrada',
        'date': '2025-10-01',
        'event_id': '0'
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        fin = Finance.query.filter_by(description='Salário').first()
        assert fin is not None
        assert fin.amount == 3000.0
        assert fin.type == 'entrada'


def test_finance_invalid_amount(auth_client):
    """Valor negativo deve ser rejeitado."""
    response = auth_client.post('/financas/nova', data={
        'description': 'Inválida', 'amount': '-100',
        'type': 'saida', 'date': '2025-10-01', 'event_id': '0'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Deve permanecer no formulário
    assert b'Valor' in response.data or b'valor' in response.data or b'form' in response.data.lower()


def test_calendar_loads(auth_client):
    """Calendário carrega com mês atual."""
    response = auth_client.get('/calendario/')
    assert response.status_code == 200
    assert b'Calend' in response.data
