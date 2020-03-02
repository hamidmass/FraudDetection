from gvo.models.user import User
from sqlalchemy_utils import PhoneNumber, CountryType


def test_new_user():
    user = User(email='BobMarley@gmail.com', phone_number=PhoneNumber('0401234567', 'FI'),
                first_name='Bob', last_name='Marley', identification_filename="", civility="",
                street="", zip="", city="", country=CountryType("JM"),
                credit=None, credit_currency=None, firebase_id=1)
    assert user.email == 'BobMarley@gmail.com'
    assert user.first_name == 'Bob'
    print(user.phone_number.e164)
    assert user.phone_number.e164 == '+358401234567'
    assert user.phone_number.international == '+358 40 1234567'
