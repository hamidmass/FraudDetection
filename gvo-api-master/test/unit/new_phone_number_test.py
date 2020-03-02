from gvo.models import phone_number
from sqlalchemy_utils import PhoneNumber


def test_new_phone_number():
    phone_number_2 = phone_number.PhoneNumber(
        phone_number='12345678910',
        user_id_assigned=0,
        forward_number='10987654321',
        mail='test@gmail.com',
        auto_renewal=True
    )
    assert phone_number_2.phone_number == "12345678910"
