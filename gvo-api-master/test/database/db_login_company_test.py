import urllib


def test_login_and_company_creation(app_flask):
    client = app_flask.test_client()

    payload = {
        'username': 'ComapnyMail101@gmail.com',
        'password': 'companyPassword',
        'name': 'Company123',
        'email': 'BobMarley@gmail.com',
        'phone_number': '040123456710',
        'phone_number_nationality': 'FI',
        'civility': '',
        'street': '',
        'zip': '',
        'city': '',
        'country': 'FI'
    }
    resp2 = client.post('/add_company?' + urllib.parse.urlencode(payload))
    print("Add Company got resp: " + str(resp2.get_json()))


def test_login_and_add_company_user(app_flask):
    client = app_flask.test_client()

    # Assuming that the user previously created
    payload = {
        'username': 'hey12@gmail.com',
        'password': 'testtest',
    }
    resp = client.post('/login?' + urllib.parse.urlencode(payload))
    print("Login got resp: " + str(resp.get_json()))
    access_token = resp.get_json()["access_token"]

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    # Also assuming we have created some users in the database
    payload2 = {
        'company_id': 0,
        'user_id': 0,
    }

    resp2 = client.post('/get_company?' + urllib.parse.urlencode(payload2), headers=headers)
    print("Add Company got resp: " + str(resp2.get_json()))