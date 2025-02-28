import pytest

def test_index(client):
    """Test que la page d'accueil est accessible"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

# Tester la route showSummary
def test_ShowSummary(client, email_auth_data, competitions_data):
    email = email_auth_data["email"]
    competition = competitions_data[0]["name"]
    rv = client.post('/showSummary', data={'email': email,
                                           'competition': competition})
    print("test_ShowSummary : OK")
    assert rv.status_code == 200
    assert b"Welcome" in rv.data

def test_showTablePoint(client, email_auth_data, competitions_data):
    rv = client.get('/showTablePoint')
    response_data = rv.data.decode('utf-8')
    print("test_showTablePoint : OK")
    assert rv.status_code == 200
    assert "Clubs" in response_data
    assert "Compétitions" in response_data

