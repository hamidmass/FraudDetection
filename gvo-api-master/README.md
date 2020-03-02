# gvo-api

### Setup PostgreSQL
```terminal
createdb gvoapi
```

### Setup virtual environment
```terminal
cd gvo-api
virtualenv env
source env/bin/activate
```

### Store Requirements
```terminal
pip freeze > requirements.txt
```

### Install Requirements
```terminal
pip install -r requirements.txt
```

### Migrate Database
```terminal
export PYTHONPATH=.
python gvo/manage.py db init
python gvo/manage.py db migrate
# You might need to add import 
# of sqlalchemy_utils in the generatedfile
# in the versions directory
python gvo/manage.py db upgrade
```

## Start Server
```terminal
python gvo/manage.py runserver
```

## Unit test
```terminal
pytest --setup-show test/unit
```

### With print statements
```terminal
pytest --setup-show test/unit -s
```

## DB test
```terminal
pytest --setup-show test/database/db_transaction_test.py
```

## Calls
### Login
Used to get a Token for a registered User.

**URL** : 
`/login`

**Method** : 
`POST`

**Data constraints**

```json
{
    "firebase_id": "[valid firebase id]"
}
```
#### Success Response

**Code** : 
`200 OK`

**Content**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzU0MTE1ODAsIm5iZiI6MTU3NTQxMTU4MCwianRpIjoiZGVhYTg3YzktYzBlMi00OWYzLWFmZmEtNTgxMzI0OGViNmUwIiwiZXhwIjoxNTc1NDEyNDgwLCJpZGVudGl0eSI6InNKbWR6QXZvQ3FjVGt5VVk0MlhXV0txTjNKeDEiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.O2IyLQZOVGz6Xgz0qAa4M1pYwuYn3I2_3S0z0q7VTHU",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzU0MTE1ODAsIm5iZiI6MTU3NTQxMTU4MCwianRpIjoiYjYzMGFjZTQtNDNmNi00ZTgyLWIzYzctMjQxYzc2OTExMmMwIiwiZXhwIjoxNTc4MDAzNTgwLCJpZGVudGl0eSI6InNKbWR6QXZvQ3FjVGt5VVk0MlhXV0txTjNKeDEiLCJ0eXBlIjoicmVmcmVzaCJ9.0yTRSkXjCzqNRRKbYAPWHSsYKQIrEjOx1Y63JW1APf0"
}
```

#### Error Response

**Condition** : If 'username' and 'password' combination is missing or invalid.

**Code** : 
`400 BAD REQUEST`

**Content** :

```json
{
    "msg": "Missing/Wrong ..."
}
```

### Search Phone
Used to get available phones to buy.

**URL** :
`/phone`

**Method** :
`GET`

**Data constraints**
`Params`
```
"country_code": "[valid country code]",
"fax_enabled": "[True or nothing]"
"sms_enabled": "[True or nothing]"
"voice_enabled": "[True or nothing]"
"type": "[local, mobile or toll free. Default = local]"
```
#### Success Response

**Code** :
`200 OK`

**Content**

```json
{
    "Phones": [
        {
            "address_requirements": "none",
            "capabilities": {
                "MMS": true,
                "SMS": true,
                "fax": true,
                "voice": true
            },
            "phone_number": "+12677744117",
            "region": "PA"
        },
        {
            "address_requirements": "none",
            "capabilities": {
                "MMS": true,
                "SMS": true,
                "fax": true,
                "voice": true
            },
            "phone_number": "+16144678210",
            "region": "OH"
        },
        {
            "address_requirements": "none",
            "capabilities": {
                "MMS": true,
                "SMS": true,
                "fax": true,
                "voice": true
            },
            "phone_number": "+18436054816",
            "region": "SC"
        }
    ]
}
```

#### Error Response

**Condition** : If 'country_code' is invalid or Twilio does not have it.

**Code** :
`404 BAD REQUEST`

**Content** :

```json
{
    "error": {
        "message": [
            "Unable to fetch page",
            "HTTP 404 {\"code\": 20404, \"message\": \"The requested resource /2010-04-01/Accounts/ACda699789aa1bb838873ae301d4863ee9/AvailablePhoneNumbers/UK/Local.json was not found\", \"more_info\": \"https://www.twilio.com/docs/errors/20404\", \"status\": 404}"
        ],
        "type": "TwilioException"
    },
    "success": false
}
```

### Buy Phone
Used to buy a phone.

**URL** :
`/phone`

**Method** :
`POST`

**Data constraints**
`Form`
```
"phone_number": "[the phone number to buy]",
"phone_type": "[fax or voice]"
"forward_number": "[forward number or nothing]"
"mail": "[email or nothing]"
```
#### Success Response

**Code** :
`204 OK`

**No Content**

#### Error Response

**Condition** : If 'phone_number' is invalid or unavailable.

**Code** :
`404 BAD REQUEST`

**Content** :

```json
{
    "error": {
        "message": [],
        "type": "TwilioException"
    },
    "success": false
}
```

### Update phone number
Used to update a phone number.

**URL** :
`/phone`

**Method** :
`PUT`

**Data constraints**
`Form`
```
"phone_number": "[the phone number to update]",
"phone_type": "[fax or voice]"
"forward_number": "[forward number or nothing]"
"mail": "[email or nothing]"
```

#### Success Response

**Code** :
`204 OK`

**No Content**

#### Error Response

**Condition** : If 'phone_number' is invalid.

**Code** :
`404 BAD REQUEST`

**Content** :

```json
{
    "error": {
        "message": [
            "The phone number does not exists"
        ],
        "type": "NonExistentPhoneError"
    },
    "success": false
}
```

### Delete phone numbers
Used to delete a phone number.

**URL** :
`/phone`

**Method** :
`DELETE`

**Data constraints**
`Form`
```
"phone_number": "[the phone number to delete]",
```

#### Success Response

**Code** :
`204 OK`

**No Content**

#### Error Response

**Condition** : If 'phone_number' is invalid.

**Code** :
`404 BAD REQUEST`

**Content** :

```json
{
    "error": {
        "message": [
            "The phone number does not exists"
        ],
        "type": "NonExistentPhoneError"
    },
    "success": false
}
```

### Make a call
Used to make a start a call from a phone.

**URL** :
`/outbound-call`

**Method** :
`POST`

**Data constraints**
`Form`
```
"From": "[the phone number that starts the phone call]",
"To": "[the destination phone number]"
```
#### Success Response

**Code** :
`204 OK`

**No Content**

#### Error Response

**Condition** : If 'From' is invalid.

**Code** :
`404 BAD REQUEST`

**Content** :

```json
{
    "error": {
        "message": [
            "The phone number does not exists"
        ],
        "type": "NonUserPhoneError"
    },
    "success": false
}
```



### Send Fax
Used to send a fax.

**URL** :
`/fax/send`

**Method** :
`POST`

**Data constraints**
`Form`
```
"origin_phone": "[the phone that is sending the fax]",
"destination_phone": "[the phone that will receive the fax]"
"fax_message": "[the url of the fax file]"
```
#### Success Response

**Code** :
`200 OK`

**No Content**

#### Error Response

**Condition** : If 'origin_phone' is invalid.

**Code** :
`404 BAD REQUEST`

**Content** :

```json
{
    "error": {
        "message": [
            "The phone number does not exists"
        ],
        "type": "NonExistentPhoneError"
    },
    "success": false
}
```

### Send SMS
Used to send a sms.

**URL** :
`/sms/send`

**Method** :
`POST`

**Data constraints**
`Form`
```
"origin_phone": "[the phone that is sending the fax]",
"destination_phone": "[the phone that will receive the fax]"
"sms": "the text of the sms"
```
#### Success Response

**Code** :
`200 OK`

**No Content**

#### Error Response

**Condition** : If 'origin_phone' is invalid.

**Code** :
`404 BAD REQUEST`

**Content** :

```json
{
    "error": {
        "message": [
            "The phone number does not exists"
        ],
        "type": "NonExistentPhoneError"
    },
    "success": false
}
```

### Get phone numbers
Used to get the phone numbers.

**URL** :
`/user/phone`

**Method** :
`GET`

**Data constraints**
`Params`
```
"phone_type": "[fax or voice]",
```

#### Success Response

**Code** :
`200 OK`

**Content**

```json
{
    "phones": [
        {
            "id": 1,
            "phone_number": "+16144678210",
            "user_id_assigned": 1,
            "forward_number": "None",
            "mail": "test@gmail.com",
            "auto_renewal": "True",
            "sid": "PN79ysi989",
            "is_fax": "False"
        },
        {
            "id": 1,
            "phone_number": "+16144678210",
            "user_id_assigned": 1,
            "forward_number": "+16144678215",
            "mail": "None",
            "auto_renewal": "True",
            "sid": "PN79ysi989",
            "is_fax": "False"
        }
    ]
}
```
