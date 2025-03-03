from datetime import datetime
import json
from pathlib import Path
from flask import Flask,render_template,request,redirect,flash,url_for

BASE_DIR = Path(__file__).resolve().parent

CLUB_PATH = BASE_DIR / "datas" / "clubs.json"
COMPETITIONS_PATH = BASE_DIR / "datas" / "competitions.json"

def loadClubs():
    with open(CLUB_PATH) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open(COMPETITIONS_PATH) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

def validate_email(email):
    # Check if the email exists in the 'clubs' list
    return any(club['email'] == email for club in clubs)

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']

    # Use the validate_email function to check if the email exists
    if not validate_email(email):
        flash("Invalid email address. Please try again.")
        return redirect(url_for('index'))  # or redirect to a specific error page

    # Find the club that matches the email
    club = [club for club in clubs if club['email'] == email][0]

    # If club is found, render the summary page
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/showTablePoint')
def showTablePoint():
    clubs = loadClubs()
    competitions = loadCompetitions()
    return render_template('tablepoint.html', clubs=clubs, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Vérification si la compétition est passée
    if competition_is_over_or_not(competition):
        flash("Cette compétition est déjà passée. Vous ne pouvez plus réserver de places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification de la limite de 12 places
    error_message = validate_places_required(club, competition, placesRequired)
    if error_message is not True:
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions)

    # Si toutes les conditions sont respectées, réserver les places
    deduct_competition_places(competition, placesRequired)
    deduct_club_points(club, placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

def competition_is_over_or_not(competition):
    """ Vérifie si la compétition est déjà passée """
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date > datetime.now():
        return True
    return False

def validate_places_required(club, competition, placesRequired):
    try:
        placesRequired = int(placesRequired)
        competition_places = int(competition['numberOfPlaces'])
        club_points = int(club['points'])
        booked = int(club.get('reservations', {}).get(competition['name'], 0))
    except ValueError:
        return False

    total_reserved = booked + placesRequired

    if total_reserved > 12:
        return False
    elif placesRequired <= 0:
        return False
    elif competition_places < placesRequired:
        return False
    elif club_points < placesRequired:
        return False
    else:
        return True

def deduct_competition_places(competition, placesRequired):
    """
    Réduit le nombre de places disponibles pour une compétition.
    Args:
    - competition (dict) : Dictionnaire contenant les informations de la compétition.
    - placesRequired (int) : Nombre de places à réserver.
    Returns:
    - dict : La compétition mise à jour avec le nombre de places restantes.
    """
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    return competition

def deduct_club_points(club, placesRequired):
    """
    Réduit les points du club en fonction du nombre de places réservées.
    Args:
    - club (dict) : Dictionnaire contenant les informations du club.
    - placesRequired (int) : Nombre de places à réserver.
    Returns:
    - dict : Le club mis à jour avec les points restants.
    """
    club['points'] = int(club['points']) - int(placesRequired)
    return club

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))