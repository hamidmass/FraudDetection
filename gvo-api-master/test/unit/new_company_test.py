from gvo.models.company import Company
from sqlalchemy_utils import PhoneNumber, CountryType


def test_new_company():
    user = Company(
            name='TestCompany',
            email='test@gmail.com',
            street='Street',
            zip='1337',
            city='Rennes',
            country=CountryType('FR'),
            phone_number=PhoneNumber('12345678910', 'FR'),
            vat_number=0,
            firebase_id_company=0
        )
    assert user.name == 'TestCompany'
    assert user.email == 'test@gmail.com'
    assert user.firebase_id_company == 0
