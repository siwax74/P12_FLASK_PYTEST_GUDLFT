from datetime import datetime
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, flash, url_for

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
    return any(club['email'] == email for club in clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    if not validate_email(email):
        flash("Invalid email address. Please try again.")
        return redirect(url_for('index'))

    club = get_club_by_email(email)
    if not competitions:
        flash("No competitions available.")
        return redirect(url_for('index'))

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/showTablePoint')
def showTablePoint():
    return render_template('tablepoint.html', clubs=clubs, competitions=competitions)

# Helper function to check if the competition date has passed
def competition_is_over(competition):
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    return competition_date < datetime.now()

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = get_club_by_name(club)
    foundCompetition = get_competition_by_name(competition)

    if foundClub and foundCompetition:
        # Check if the competition has already passed using the helper function
        if competition_is_over(foundCompetition):
            flash("Cette compétition est déjà passée. Vous ne pouvez plus réserver de places.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)

        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - please try again.")
        return render_template('welcome.html', club=club, competitions=competitions)

def get_club_by_name(name):
    return next((c for c in clubs if c['name'] == name), None)

def get_club_by_email(email):
    return next((c for c in clubs if c['email'] == email), None)

def get_competition_by_name(name):
    
    return next((c for c in competitions if c['name'] == name), None)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = get_competition_by_name(request.form['competition'])
    club = get_club_by_name(request.form['club'])
    placesRequired = int(request.form['places'])

    error_message = validate_places_required(club, competition, placesRequired)
    if error_message is not True:
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions)

    deduct_competition_places(competition, placesRequired)
    deduct_club_points(club, placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)



def validate_places_required(club, competition, placesRequired):
    try:
        placesRequired = int(placesRequired)
        competition_places = int(competition['numberOfPlaces'])
        club_points = int(club['points'])
        booked = int(club.get('reservations', {}).get(competition['name'], 0))
    except ValueError:
        return "Invalid number of places requested."

    total_reserved = booked + placesRequired

    if placesRequired <= 0:
        return "Le nombre de places doit être supérieur à zéro."
    if total_reserved > 12:
        return "Vous ne pouvez pas réserver plus de 12 places par compétition."
    if competition_places < placesRequired:
        return "Pas assez de places disponibles pour cette compétition."
    if club_points < placesRequired:
        return "Pas assez de points pour réserver ces places."

    return True


def deduct_competition_places(competition, placesRequired):
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    return competition


def deduct_club_points(club, placesRequired):
    club['points'] = int(club['points']) - placesRequired
    return club


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
