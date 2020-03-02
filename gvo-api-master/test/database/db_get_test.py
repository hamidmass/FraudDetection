import urllib


def test_get_users(app_flask):
    client = app_flask.test_client()

    # Assuming that the user was previously created
    payload = {
        'username': 'BobMarley@gmail.com',
        'password': 'testtest',
    }
    resp = client.post('/login?' + urllib.parse.urlencode(payload))
    print("Login got resp: " + str(resp.get_json()))
    access_token = resp.get_json()["access_token"]

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    resp2 = client.get('/users', headers=headers)
    print("Got users: " + str(resp2.get_json()))


def test_get_companies(app_flask):
    client = app_flask.test_client()

    # Assuming that the user was previously created
    payload = {
        'username': 'BobMarley@gmail.com',
        'password': 'testtest',
    }
    resp = client.post('/login?' + urllib.parse.urlencode(payload))
    print("Login got resp: " + str(resp.get_json()))
    access_token = resp.get_json()["access_token"]

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    # Add a company
    payload = {
        'username': 'Bob13@gmail.com',
        'password': 'companyPassword',
        'name': 'Bob',
        'email': 'Bob@gmail.com',
        'phone_number': '040123456710',
        'phone_number_nationality': 'FI',
        'civility': '',
        'street': '',
        'zip': '',
        'city': '',
        'country': 'FI',
        'vat_number': 123
    }

    resp2 = client.post('/add_company?' + urllib.parse.urlencode(payload))
    print("Add Company got resp: " + str(resp2.get_json()))

    payload2 = {
        'name': 'Bob'
    }

    # Check we receives the same company Back
    resp2 = client.get('/get_company_by_name?' + urllib.parse.urlencode(payload2), headers=headers)
    print("Got companies: " + str(resp2.get_json()))


