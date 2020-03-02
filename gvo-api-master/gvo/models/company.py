from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy_utils import CountryType, PhoneNumberType


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, index=True, nullable=False)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    street = db.Column(db.String, index=True, nullable=False)
    zip = db.Column(db.String, unique=True, index=True, nullable=False)
    city = db.Column(db.String, index=True, nullable=False)
    country = db.Column(CountryType, index=True, nullable=False)
    phone_number = db.Column(PhoneNumberType, index=True, nullable=False)
    vat_number = db.Column(db.Integer, unique=True, index=True, nullable=False)
    firebase_id_company = db.Column(db.String, index=True, unique=True)

    # Relationships
    phone_number_owner_company = relationship('PhoneNumberOwnerCompany', back_populates="company")
    company_user = relationship('CompanyUser', back_populates="company")
    subscription_company = relationship('SubscriptionCompany', back_populates="company")
    transaction_company = relationship('TransactionCompany', back_populates="company")
    phone_number_transaction_company = relationship('PhoneNumberTransactionCompany', back_populates="company")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'street': self.street,
            'zip': self.zip,
            'country': str(self.country),
            'phone_number': str(self.phone_number),
            'vat_number': self.vat_number,
            'firebase_id_company': self.vat_number
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_name(cls, name_2):
        return cls.query.filter_by(name=name_2).first()

    @classmethod
    def get_all_companies(cls):
        return cls.query.all()
