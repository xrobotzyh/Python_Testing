from server import loadClubs, loadCompetitions


def test_loadClubs():
    # setup
    file_loadclubs = loadClubs()
    # Action
    expected_value = 3
    # assert
    assert len(file_loadclubs) == expected_value


def test_loadCompetitions():
    file = loadCompetitions()

    expected_value = 2

    assert len(file) == expected_value


def test_index(client):
    response = client.get('/')

    assert response.status_code == 200


def test_showSummary_with_validate_email(client):
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})

    assert b'Welcome' in response.data
    assert response.status_code == 200


def test_showSummary_with_unvalidate_email(client):
    response = client.post('/showSummary', data={'email': '11@irontemple.com'})

    assert b'The email is not found' in response.data
    assert response.status_code == 401


def test_book_valid_competition(client, validate_club, validate_competition):
    competition = validate_competition['name']
    club = validate_club['name']
    places_available = validate_competition['numberOfPlaces']

    response = client.get(f'/book/{competition}/{club}')

    assert f'Places available: {places_available}'.encode() in response.data
    assert response.status_code == 200


def test_book_competition_finished(client, validate_club, competition_past):
    competition = competition_past['name']
    club = validate_club['name']

    response = client.get(f'/book/{competition}/{club}')

    assert response.status_code == 403
    assert b'The competition is finished !' in response.data


def test_purchasePlaces_sucess(client, validate_club, validate_competition):
    competition = validate_competition['name']
    club = validate_club['name']
    competition_places = validate_competition['numberOfPlaces']
    club_points = validate_club['points']
    places_required = 2
    competition_places = int(competition_places) - places_required
    club_points = int(club_points) - places_required

    response = client.post(f'/purchasePlaces',
                           data={'competition': competition, 'club': club, 'places': places_required})

    assert response.status_code == 200
    assert f'Number of Places: {competition_places}'.encode() in response.data
    assert f'Points available: {club_points}'.encode() in response.data


def test_purchsePlaces_more_than_12_places(client, validate_club, validate_competition):
    competition = validate_competition['name']
    club = validate_club['name']
    places_required = 13

    response = client.post(f'/purchasePlaces',
                           data={'competition': competition, 'club': club, 'places': places_required})

    assert response.status_code == 403
    assert b'You can not reserve more than 12 places' in response.data


def test_purchsePlaces_more_than_places_availables(client, validate_clubs_points_less_than_12, validate_competition):
    competition = validate_competition
    club = validate_clubs_points_less_than_12
    places_required = int(club['points']) + 1

    response = client.post(f'/purchasePlaces',
                           data={'competition': competition['name'], 'club': club['name'], 'places': places_required})

    assert response.status_code == 403
    assert b'You do not have enough points to reserve the places' in response.data


def test_show_club_points(client):
    response = client.get(f'/show_club_points')

    assert response.status_code == 200
    assert b'Lists of clubs and their points || GUDLFT' in response.data


def logout(client):
    response = client.get(f'/logout')

    assert response.status_code == 200
