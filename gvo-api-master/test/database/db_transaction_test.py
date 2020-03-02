import urllib


def test_transaction(app_client_with_user):
    # Assuming that the user was previously created
    # in Firebase
    payload = {
        'firebase_id': '123456789',
    }
    resp = app_client_with_user.post('/login?' + urllib.parse.urlencode(payload))
    print("Login got resp: " + str(resp.get_json()))
    access_token = resp.get_json()["access_token"]

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    # Find a user in the database
    resp2 = app_client_with_user.get('/users', headers=headers)
    print("Got users: " + str(resp2.get_json()))

    # Using the first user here just for testing purpose
    user_id = resp2.get_json()['users'][0]['id']

    # Setup an historical service price
    payload = {
        'service_name_enum': '1',
        'country': 'FI',
        'region': 'Helsinki',
        'time_epoch': '1575663571',
        'price': 1,
        'currency': 'USD'
    }

    resp3 = app_client_with_user.post('/historical_service_price?' + urllib.parse.urlencode(payload), headers=headers)
    print("Got response from historical Service price : " + str(resp3.get_json()))

    # Get the historical service price
    resp4 = app_client_with_user.get('/get_all_service_prices', headers=headers)
    print("Got historical service prices: " + str(resp4.get_json()))

    # Using the first historical service price here just for testing purpose
    service_price_id = resp4.get_json()['service_prices'][0]['id']

    # Insert transaction for user
    # Here for the Fax Sending service
    payload = {
        'user_id': str(user_id),
        'service_name_enum': '1',
        'user_id_assigned': '1',
        'phone_number': '040123456710',
        'phone_number_nationality': 'FI',
        'mail': 'BobMarley@gmail.com',
        'historical_service_price_id': str(service_price_id),
        'country': 'FI',
        'region': 'Test',
        'start_time': '1575663572',
        'end_time': '1575669572'
    }

    resp5 = app_client_with_user.post('/transaction_user?' + urllib.parse.urlencode(payload), headers=headers)
    print("Got response from user transaction: " + str(resp5.get_json()))

    # Try to get the transaction
    resp6 = app_client_with_user.get('/get_transaction_user_by_id', headers=headers)
    print("Got historical service prices: " + str(resp6.get_json()))

    assert resp6.get_json()['transaction']['country'] == 'Finland'


