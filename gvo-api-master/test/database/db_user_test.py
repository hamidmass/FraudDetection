from flask import json
import urllib


def test_user_creation(app_flask):

    client = app_flask.test_client()
    payload = {
        'email': 'BobMarley@gmail.com',
        'phone_number': '040123456710',
        'phone_number_nationality': 'FI',
        'first_name': 'Bob',
        'last_name': 'Marley',
        'civility': '',
        'street': '',
        'zip': '',
        'city': '',
        'country': 'FI',
        'credit': 0,
        'credit_currency': 'USD'
    }
    resp = client.post('/add_user?' + urllib.parse.urlencode(payload))
    print("Add user got resp: " + str(resp.get_json()))


def test_user_creation_none_currency(app_flask):

    client = app_flask.test_client()
    payload = {
        'email': 'BobMarley@gmail.com',
        'phone_number': '040123456710',
        'phone_number_nationality': 'FI',
        'first_name': 'Bob',
        'last_name': 'Marley',
        'civility': '',
        'street': '',
        'zip': '',
        'city': '',
        'country': 'FI'
    }
    resp = client.post('/add_user?' + urllib.parse.urlencode(payload))
    print("Add user got resp: " + str(resp.get_json()))