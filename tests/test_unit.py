# test_your_module.py
from src.server import get_club_by_email


def test_unit_should_return_true_if_email_is_valid(email_auth_data):
    # Utilisation de l'email de la fixture dans le test
    email = email_auth_data['email']
    result = get_club_by_email(email)
    print(f"Result of get_club_list with valid email ({email}): {result}")
    assert result['email'] == email, f"Expected email {email}, but got {result['email']}"

def test_unit_should_return_false_if_email_is_not_valid(email_auth_wrongdata):
    # Utilisation de l'email invalide de la fixture pour le test
    email = email_auth_wrongdata["email"]
    expected_value = False
    result = get_club_by_email(email)
    print(f"Result of get_club_by_email with invalid email ({email}): {result}")
    assert result == expected_value, f"Expected {expected_value}, but got {result}"

