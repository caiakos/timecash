import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///timecash.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True

    # Logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # Extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'

    # Blueprints
    from app.auth.routes import auth_bp
    from app.events.routes import events_bp
    from app.finances.routes import finances_bp
    from app.calendar.routes import calendar_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(events_bp, url_prefix='/eventos')
    app.register_blueprint(finances_bp, url_prefix='/financas')
    app.register_blueprint(calendar_bp, url_prefix='/calendario')

    # Rota raiz
    from flask import redirect, url_for
    @app.route('/')
    def index():
        return redirect(url_for('calendar.index'))

    # Criar tabelas
    with app.app_context():
        db.create_all()
        app.logger.info('Banco de dados inicializado.')

    return app
