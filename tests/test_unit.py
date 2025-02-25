# test_your_module.py
from src.server import deduct_club_points, deduct_competition_places, get_club_by_email, validate_places_required


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

def test_validate_places_required_should_return_true_if_places_available(competitions_data, clubs_data):
    competition = competitions_data[0]
    club = clubs_data[0]
    placesRequired = 5
    expected_value = True
    print("test_validate_places_required_should_return_true_if_places_available : OK")
    assert validate_places_required(club, competition, placesRequired) == expected_value

def test_validate_places_required_should_fail_when_booking_more_than_12(competitions_data, clubs_data):
    competition = competitions_data[0]
    club = clubs_data[0]
    placesRequired = 13
    expected_value = "Sorry, you can only book up to 12 places"
    print("test_validate_places_required_should_fail_when_booking_more_than_12 : OK")
    assert validate_places_required(club, competition, placesRequired) == expected_value

def test_validate_places_required_should_fail_when_booking_zero_or_less(competitions_data, clubs_data):
    competition = competitions_data[0]
    club = clubs_data[0]
    placesRequired = 0
    expected_value = "Sorry, you must book at least 1 place"
    print("test_validate_places_required_should_fail_when_booking_zero_or_less : OK")
    assert validate_places_required(club, competition, placesRequired) == expected_value

def test_validate_places_required_should_fail_when_not_enough_competition_places(competitions_data, clubs_data):
    competition = competitions_data[1]  # Seulement 3 places disponibles
    club = clubs_data[0]
    placesRequired = 5
    expected_value = "Sorry, there are not enough places available"
    print("test_validate_places_required_should_fail_when_not_enough_competition_places : OK")
    assert validate_places_required(club, competition, placesRequired) == expected_value

def test_validate_places_required_should_fail_when_club_has_insufficient_points(competitions_data, clubs_data):
    competition = competitions_data[0]
    club = clubs_data[1]  # Seulement 4 points disponibles
    placesRequired = 6
    expected_value = "Sorry, you don't have enough points to book this many places"
    print("test_validate_places_required_should_fail_when_club_has_insufficient_points : OK")
    assert validate_places_required(club, competition, placesRequired) == expected_value

def test_validate_places_required_should_fail_on_invalid_input(competitions_data, clubs_data):
    competition = competitions_data[0]
    club = clubs_data[0]
    placesRequired = "invalid"
    expected_value = "Invalid number of places or points"
    print("test_validate_places_required_should_fail_on_invalid_input : OK")
    assert validate_places_required(club, competition, placesRequired) == expected_value