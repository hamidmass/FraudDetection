import os
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

    # Upload test
    payload = {
        'email': 'BobMarley@gmail.com'
    }

    dir2 = os.path.dirname(__file__)
    fp = open(dir2 + '/TourEiffel.jpg', 'rb')
    data = dict(file=(fp, 'TourEiffel.jpg'))
    resp2 = app_client_with_user\
        .post('/upload_user_identification?' + urllib.parse.urlencode(payload),
              headers=headers,
              buffered=True,
              content_type='multipart/form-data',
              data=data)

    print("Got response from file uploading : " + str(resp2.get_json()))

    # Find a user in the database
    resp3 = app_client_with_user.get('/users', headers=headers)
    print("Got users: " + str(resp3.get_json()))



