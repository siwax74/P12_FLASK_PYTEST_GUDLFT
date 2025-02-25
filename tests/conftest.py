from src.server import app
import pytest

@pytest.fixture
def client():
    new_app = app
    new_app.testing = True
    with new_app.test_client() as c:
        yield c

@pytest.fixture
def email_auth_data():
    login = {"email": "john@simplylift.co"}
    return login

@pytest.fixture
def email_auth_wrongdata():
    login = {"email": "undefined@yopmail.com"}
    return login

@pytest.fixture
def clubs_data():
    return [

        {

            "name":"Simply Lift",

            "email":"john@simplylift.co",

            "points":"13"

        },

        {

            "name":"Iron Temple",

            "email": "admin@irontemple.com",

            "points":"4"

        },

        {   "name":"She Lifts",

            "email": "kate@shelifts.co.uk",

            "points":"12"

        }

    ]

@pytest.fixture
def competitions_data():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "3"
        }
    ]
