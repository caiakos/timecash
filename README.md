# TimeCash 💰⏱
Gestão integrada de tempo e finanças pessoais.

🌐 **Acesse online:** https://timecash.onrender.com

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
- Bootstrap 5.3 (framework CSS)
- PostgreSQL (produção) / SQLite (desenvolvimento)
- Jinja2 (templates)
- Gunicorn (servidor de produção)

## Como rodar

### 1. Clonar o projeto

```bash
git clone https://github.com/caiakos/timecash.git
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

Crie um arquivo `.env` na raiz com:
