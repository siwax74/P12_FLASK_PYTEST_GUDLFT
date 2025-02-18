import pytest

def test_index(client):
    """Test que la page d'accueil est accessible"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

# Tester la route showSummary
def test_show_summary(client, email_auth_data, competitions_data):
    email = email_auth_data["email"]
    competition = competitions_data[0]["name"]
    rv = client.post('/showSummary', data={'email': email,
                                           'competition': competition})
    assert rv.status_code == 200
    assert b"Welcome" in rv.data