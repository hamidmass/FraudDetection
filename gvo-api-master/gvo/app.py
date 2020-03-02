import os

import pyrebase as pyrebase
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from distutils.util import strtobool
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = bool(strtobool(os.getenv('DEBUG')))
app.config['TESTING'] = bool(strtobool(os.getenv('TESTING')))
app.config['CSRF_ENABLED'] = bool(strtobool(os.getenv('CSRF_ENABLED')))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Needed to add support for Cors, used by fetch in React
CORS(app)
db = SQLAlchemy(app)

# Setup Firebase
config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": "authdemo-696ae.firebaseapp.com",
    "databaseURL": "https://authdemo-696ae.firebaseio.com",
    "storageBucket": "authdemo-696ae.appspot.com"
}
firebase = pyrebase.initialize_app(config)

# Setup JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Setup Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_MAX_EMAILS'] = 1
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

from gvo.models.twilio import Twilio
from gvo.models.mail_sender import MailSender

twilio = Twilio()
email_sender = MailSender()

from gvo.resources.twilio_fax import twilio_fax
from gvo.resources.twilio_phone import twilio_phone
from gvo.resources.twilio_call import twilio_call
from gvo.resources.error_handler import error_handler
from gvo.resources.user_registration import user_registration_route
from gvo.resources.user_query import users
from gvo.resources.user_login import user_login
from gvo.resources.user_refresh import user_refresh
from gvo.resources.company import company_route
from gvo.resources.historical_service_price import historical_service_price_route
from gvo.resources.phone_number_owner import phone_number_owner_route
from gvo.resources.phone_number_registration import phone_number_registration_route
from gvo.resources.phone_number_transaction import phone_number_transaction_route
from gvo.resources.prepaid_account import prepaid_account_route
from gvo.resources.subscription import subscription_route
from gvo.resources.transaction import transaction_route
from gvo.resources.phone_number import phone_number
from gvo.resources.twilio_sms import twilio_sms


app.register_blueprint(user_registration_route)
app.register_blueprint(users)
app.register_blueprint(user_login)
app.register_blueprint(user_refresh)
app.register_blueprint(company_route)
app.register_blueprint(historical_service_price_route)
app.register_blueprint(phone_number_owner_route)
app.register_blueprint(phone_number_registration_route)
app.register_blueprint(phone_number_transaction_route)
app.register_blueprint(prepaid_account_route)
app.register_blueprint(subscription_route)
app.register_blueprint(transaction_route)
app.register_blueprint(twilio_fax)
app.register_blueprint(twilio_phone)
app.register_blueprint(twilio_call)
app.register_blueprint(twilio_sms)
app.register_blueprint(phone_number)
app.register_blueprint(error_handler)

if __name__ == '__main__':
    app.run()


