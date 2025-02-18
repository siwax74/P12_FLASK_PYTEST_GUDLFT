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

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


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
    if placesRequired < 1 or placesRequired > 12:
        flash("Please enter a number between 1 and 12")
        return render_template('welcome.html', club=club, competitions=competitions)
    # Vérification de la disponibilité des places
    if placesRequired > int(competition['numberOfPlaces']):
        flash(f"Not enough places available. Only {competition['numberOfPlaces']} places left.")
        return render_template('welcome.html', club=club, competitions=competitions)
    if int(competition['numberOfPlaces']) < 0:
        flash(f"{competition['numberOfPlaces']}, is full.")
    # Si toutes les conditions sont respectées, réserver les places
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - int(placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))