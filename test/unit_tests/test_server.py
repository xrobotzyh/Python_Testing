from server import loadClubs, loadCompetitions


def test_loadClubs(validate_club):
    file_loadclubs = loadClubs()

    assert validate_club in file_loadclubs


def test_loadCompetitions(validate_competition):
    file = loadCompetitions()

    assert validate_competition in file


def test_index(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


class TestshowSummary:
    def test_showSummary_with_validate_email(self, client):
        response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})

        assert b'Welcome' in response.data
        assert response.status_code == 200

    def test_showSummary_with_unvalidate_email(self, client):
        response = client.post('/showSummary', data={'email': '11@irontemple.com'})

        assert b'The email is not found' in response.data
        assert response.status_code == 401


class Testbook:
    def test_book_valid_competition(self, client, validate_club, validate_competition):
        competition = validate_competition['name']
        club = validate_club['name']
        places_available = validate_competition['numberOfPlaces']

        response = client.get(f'/book/{competition}/{club}')

        assert f'Places available: {places_available}'.encode() in response.data
        assert response.status_code == 200

    def test_book_competition_finished(self, client, validate_club, competition_past):
        competition = competition_past['name']
        club = validate_club['name']

        response = client.get(f'/book/{competition}/{club}')

        assert response.status_code == 403
        assert b'The competition is finished !' in response.data


class TestpurchasePlaces:
    def test_purchasePlaces_sucess(self, client, validate_club, validate_competition):
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

    def test_purchsePlaces_more_than_12_places(self, client, validate_club, validate_competition):
        competition = validate_competition['name']
        club = validate_club['name']
        places_required = 13

        response = client.post(f'/purchasePlaces',
                               data={'competition': competition, 'club': club, 'places': places_required})

        assert response.status_code == 403
        assert b'You can not reserve more than 12 places' in response.data

    def test_purchsePlaces_more_than_places_availables(self, client, validate_clubs_points_less_than_12,
                                                       validate_competition):
        competition = validate_competition
        club = validate_clubs_points_less_than_12
        places_required = int(club['points']) + 1

        response = client.post(f'/purchasePlaces',
                               data={'competition': competition['name'], 'club': club['name'],
                                     'places': places_required})

        assert response.status_code == 403
        assert b'You do not have enough points to reserve the places' in response.data


def test_show_club_points(client):
    response = client.get(f'/show_club_points')

    assert response.status_code == 200
    assert b'Lists of clubs and their points || GUDLFT' in response.data


def logout(client):
    response = client.get(f'/logout')

    assert response.status_code == 200
