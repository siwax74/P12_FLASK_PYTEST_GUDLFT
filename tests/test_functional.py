import pytest

def test_index(client):
    """Test que la page d'accueil est accessible"""
    # Cas où tout est correct
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_ShowSummary(client, email_auth_data, competitions_data):
    # Cas où tout est correct
    email = email_auth_data["email"]
    competition = competitions_data[0]["name"]
    rv = client.post('/showSummary', data={'email': email,
                                           'competition': competition})
    print("test_ShowSummary : OK")
    assert rv.status_code == 200
    assert b"Welcome" in rv.data

def test_showTablePoint(client):
    # Cas où tout est correct
    rv = client.get('/showTablePoint')
    response_data = rv.data.decode('utf-8')
    print("test_showTablePoint : OK")
    assert rv.status_code == 200
    assert "Clubs" in response_data
    assert "Compétitions" in response_data

def test_book(client, competitions_data, clubs_data):
    # Cas où tout est correct
    competition = competitions_data[0]
    club = clubs_data[0]
    rv = client.get(f'/book/{competition["name"]}/{club["name"]}')
    print("test_book : OK")
    response_data = rv.data.decode('utf-8')
    assert rv.status_code == 200
    assert "Spring Festival" in response_data
    assert "Simply Lift" in response_data

def test_purchase_places(client, competitions_data, clubs_data):
    # Cas où tout est correct
    club = clubs_data[0]
    competition = competitions_data[0]
    places_required = 4
    rv = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': places_required
    })
    print("test_purchase_places : OK")
    assert rv.status_code == 200
    assert b"Great-booking complete!" in rv.data

def test_logout(client):
    """Test de déconnexion de l'utilisateur"""
    # Tester la déconnexion
    rv = client.get('/logout')
    assert rv.status_code == 302
    assert rv.headers['Location'] == '/'