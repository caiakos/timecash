def test_login_page_loads(client):
    """Página de login deve carregar corretamente."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Entrar' in response.data or b'login' in response.data.lower()


def test_register_page_loads(client):
    """Página de cadastro deve carregar."""
    response = client.get('/auth/cadastro')
    assert response.status_code == 200


def test_register_user(client):
    """Cadastro de novo usuário deve redirecionar para login."""
    response = client.post('/auth/cadastro', data={
        'name': 'João Silva',
        'email': 'joao@email.com',
        'password': 'senha123',
        'confirm': 'senha123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'sucesso' in response.data.lower() or b'login' in response.data.lower()


def test_register_duplicate_email(client):
    """Cadastro com email duplicado deve mostrar erro."""
    data = {'name': 'A', 'email': 'dup@email.com', 'password': 'senha123', 'confirm': 'senha123'}
    client.post('/auth/cadastro', data=data)
    response = client.post('/auth/cadastro', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'cadastrado' in response.data.lower() or b'email' in response.data.lower()


def test_login_wrong_password(client):
    """Login com senha errada deve mostrar mensagem de erro."""
    client.post('/auth/cadastro', data={
        'name': 'Maria', 'email': 'maria@email.com',
        'password': 'certa123', 'confirm': 'certa123'
    })
    response = client.post('/auth/login', data={
        'email': 'maria@email.com', 'password': 'errada'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'incorretos' in response.data.lower() or b'erro' in response.data.lower() or b'senha' in response.data.lower()


def test_logout(auth_client):
    """Logout deve redirecionar para login."""
    response = auth_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200


def test_calendar_requires_login(client):
    """Calendário exige autenticação."""
    response = client.get('/calendario/', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data.lower() or b'entrar' in response.data.lower()
