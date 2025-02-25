# test_your_module.py
from src.server import deduct_club_points, deduct_competition_places, get_club_by_email


def test_unit_should_return_true_if_email_is_valid(email_auth_data, clubs_data):
    # Utilisation de l'email invalide de la fixture pour le test
    email = email_auth_data['email']
    expected_value = clubs_data[0]
    print(f"test_unit_should_return_true_if_email_is_valid : OK")
    assert get_club_by_email(email) == expected_value

def test_unit_should_return_false_if_email_is_not_valid(email_auth_wrongdata):
    # Utilisation de l'email invalide de la fixture pour le test
    email = email_auth_wrongdata["email"]
    expected_value = False
    print(f"test_unit_should_return_false_if_email_is_not_valid : OK")
    assert get_club_by_email(email) == expected_value

def test_unit_should_return_true_if_point_club_is_deduct(clubs_data):
    # Sélectionne le premier club de la fixture
    club = clubs_data[0]  # "Simply Lift"
    placesRequired = 5
    expected_value = 8  # 13 - 5 = 8
    print(f"test_unit_should_return_true_if_point_club_is_deduct : OK")
    assert deduct_club_points(club, placesRequired)["points"] == expected_value

def test_unit_should_return_true_if_point_competition_is_deduct(competitions_data):
    # Sélectionne la première compétition de la fixture
    competition = competitions_data[0]
    placesRequired = 5
    expected_value = 20  # 25 - 5 = 20
    print(f"test_unit_should_return_true_if_point_competition_is_deduct : OK")
    assert deduct_competition_places(competition, placesRequired)["numberOfPlaces"] == expected_value

