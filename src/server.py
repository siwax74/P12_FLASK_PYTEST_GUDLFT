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

def get_club_by_email(email):
    if email:
        matching_clubs = [club for club in clubs if club['email'] == email]
        if matching_clubs:
            return matching_clubs[0]
        else:
            return False
    else:
        return False

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    # Vérification si l'email est vide
    if not email:
        flash('Please enter an email address')
        return redirect(url_for('index'))
    club = get_club_by_email(email)
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else: # BUG 3
        flash('Email not found')
        return redirect(url_for('index'))

@app.route('/showtable')
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
    # Vérification de la limite de 12 places
    error_message = validate_places_required(club, competition, placesRequired)
    if error_message is not True:
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions)
    # Si toutes les conditions sont respectées, réserver les places
    competition = deduct_competition_places(competition, placesRequired)
    club = deduct_club_points(club, placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

def validate_places_required(club, competition, placesRequired):
    try:
        placesRequired = int(placesRequired)
        competition_places = int(competition['numberOfPlaces'])
        club_points = int(club['points'])
    except ValueError:
        return "Invalid number of places or points"
    if placesRequired > 12:
        return "Sorry, you can only book up to 12 places"
    elif placesRequired <= 0:
        return "Sorry, you must book at least 1 place"
    elif competition_places < placesRequired:
        return "Sorry, there are not enough places available"
    elif club_points < placesRequired:
        return "Sorry, you don't have enough points to book this many places"
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