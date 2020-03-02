from sqlalchemy.orm import relationship
from sqlalchemy_utils import PhoneNumberType
from gvo.app import db
from sqlalchemy import ForeignKey


class PhoneNumber(db.Model):
    __tablename__ = 'phone_number'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(PhoneNumberType, index=True, nullable=True)
    user_id_assigned = db.Column(db.Integer, ForeignKey('user.id'), index=True, nullable=True)
    forward_number = db.Column(PhoneNumberType, index=True, nullable=True)
    mail = db.Column(db.String, index=True, nullable=True)
    auto_renewal = db.Column(db.Boolean, index=True, nullable=False)
    sid = db.Column(db.String, index=True, nullable=False)
    is_fax = db.Column(db.Boolean, index=True, nullable=False,default=False)

    # Relationships
    phone_number_owner_user = relationship('PhoneNumberOwnerUser', back_populates="phone_number", uselist=False)
    phone_number_owner_company = relationship('PhoneNumberOwnerCompany', back_populates="phone_number", uselist=False)
    user = relationship('User', back_populates="phone_number_2")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'phone_number': str(self.phone_number.e164),
            'user_id_assigned': self.user_id_assigned,
            'forward_number': str(self.forward_number),
            'mail': self.mail,
            'auto_renewal': self.auto_renewal,
            'sid': self.sid,
            'is_fax': self.is_fax
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone_number=phone.e164).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id_assigned=user_id)

    @classmethod
    def get_all_phone_numbers(cls):
        return cls.query.all()


