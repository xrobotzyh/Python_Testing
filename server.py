import json
from flask import Flask, render_template, request, redirect, flash, url_for, make_response
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # try to login with email,is the email is in json file,login,otherwise display a email not found message
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions), club
    except IndexError:
        flash("The email is not found.")
        response = make_response(render_template('index.html'))
        response.status_code = 401
        return response


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    # deserialize str time to object and check if the competition is past
    competition_pasted = (datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now())

    if foundClub and foundCompetition and not competition_pasted:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    elif foundClub and foundCompetition and competition_pasted:
        flash('The competition is finished !')
        response = make_response(render_template('welcome.html', club=foundClub, competitions=competitions))
        response.status_code = 403
        return response
    else:
        flash("Something went wrong-please try again")
        response = make_response(render_template('welcome.html', club=club, competitions=competitions))
        response.status_code = 400
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    points_left_club = int(club['points'])
    places_max_reserve = 12
    # if place required > 12 places
    if places_required > places_max_reserve:
        flash('You can not reserve more than 12 places')
        response = make_response(render_template('welcome.html', club=club, competitions=competitions))
        response.status_code = 403
        return response
    # if places required > points that club have
    elif places_required > points_left_club:
        flash('You do not have enough points to reserve the places')
        response = make_response(render_template('welcome.html', club=club, competitions=competitions))
        response.status_code = 403
        return response
    # normal condition, points update once places reserved
    else:
        club['points'] = int(club['points']) - places_required
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/show_club_points')
def show_club_points():
    """
    @return: return a html page that shows clubs lists and their points left
    """
    return render_template('show_clubs.html', clubs=clubs, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
