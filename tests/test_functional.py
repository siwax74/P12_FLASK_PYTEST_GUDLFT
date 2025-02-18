import pytest
from src.server import app

@pytest.fixture
def client():
    """Fixture pour configurer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test que la page d'accueil est accessible"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data
