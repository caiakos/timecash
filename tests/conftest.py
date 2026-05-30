import pytest
from app import create_app, db as _db
from app.models import User, Event, Finance
from datetime import date


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret'

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client, app):
    """Cliente autenticado com usuário de teste."""
    with app.app_context():
        user = User(name='Teste', email='teste@timecash.com')
        user.set_password('senha123')
        _db.session.add(user)
        _db.session.commit()

    client.post('/auth/login', data={'email': 'teste@timecash.com', 'password': 'senha123'})
    return client
