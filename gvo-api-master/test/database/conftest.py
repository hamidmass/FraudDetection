import pytest
from sqlalchemy_utils import PhoneNumber, Country, Currency

from gvo.app import app, db
from gvo.models import user


@pytest.fixture
def app_flask():
    return app


@pytest.fixture
def app_client_with_user():
    phone_number = PhoneNumber('040123456710', 'FI')
    country = Country(str('FI'))
    currency = Currency(str('USD'))

    user_table_insert = user.User(
        email='BobMarley@gmail.com',
        phone_number=phone_number,
        first_name='Bob',
        last_name='Marley',
        civility='',
        street='',
        zip='',
        city='',
        country=country,
        credit=0,
        credit_currency=currency,
        firebase_id="123456789"
    )

    client = app.test_client()

    # Clears the database before starting
    db.drop_all()
    db.create_all()
    db.session.commit()
    db.session.add(user_table_insert)
    db.session.commit()
    return client

