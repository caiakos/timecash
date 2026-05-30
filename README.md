# TimeCash 💰⏱

Gestão integrada de tempo e finanças pessoais.

## Integrantes
- Caio Drumond de Abreu Rebouças
- Cecília Magalhães Santos
- João Victor Sanchez Gonçalves Furtado

## Tecnologias
- Python 3.11+
- Flask 3.0
- Flask-SQLAlchemy (ORM)
- Flask-Login (autenticação)
- Flask-WTF / WTForms (formulários e validação)
- SQLite (banco de dados)
- Jinja2 (templates)

## Como rodar

### 1. Clonar o projeto
```bash
git clone <url-do-repo>
cd timecash
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Renomeie ou copie o arquivo `.env` (já está pronto com valores padrão).

### 5. Rodar o projeto
```bash
python run.py
```

Acesse: http://localhost:5000

### 6. Rodar os testes
```bash
pytest -v
```

## Estrutura do Projeto
```
timecash/
├── app/
│   ├── __init__.py         # Application Factory (create_app)
│   ├── models.py           # Modelos: User, Event, Finance
│   ├── auth/               # Blueprint de autenticação
│   │   ├── forms.py
│   │   └── routes.py
│   ├── events/             # Blueprint de eventos
│   │   ├── forms.py
│   │   └── routes.py
│   ├── finances/           # Blueprint de finanças
│   │   ├── forms.py
│   │   └── routes.py
│   ├── calendar/           # Blueprint do calendário
│   │   └── routes.py
│   ├── static/             # CSS e JS
│   └── templates/          # Templates Jinja2
├── tests/                  # Testes automatizados (pytest)
├── run.py                  # Ponto de entrada
├── .env                    # Variáveis de ambiente
└── requirements.txt
```
