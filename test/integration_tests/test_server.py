def test_login_and_purchase_places(client, validate_club, validate_competition):
    # login page
    response = client.get(f'/')

    assert response.status_code == 200

    # welcome page
    club_email = validate_club['email']

    response = client.post(f'/showSummary', data={'email': validate_club['email']})

    assert response.status_code == 200
    assert f'Welcome, {club_email}'.encode() in response.data

    # purchase page
    competition_name = validate_competition['name']
    club_name = validate_club['name']
    competition_places = validate_competition['numberOfPlaces']
    club_points = validate_club['points']
    places_required = 2
    competition_places = int(competition_places) - places_required
    club_points = int(club_points) - places_required

    response = client.post(f'/purchasePlaces',
                           data={'competition': competition_name, 'club': club_name, 'places': places_required})
    assert response.status_code == 200
    assert f'Number of Places: {competition_places}'.encode() in response.data
    assert f'Points available: {club_points}'.encode() in response.data
