from sqlalchemy import LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.util import b64encode

from gvo.app import db
from sqlalchemy_utils import CountryType, CurrencyType, PhoneNumberType


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, index=True, unique=True, nullable=False)
    phone_number = db.Column(PhoneNumberType, index=True, unique=True, nullable=False)
    first_name = db.Column(db.String, index=True, nullable=False)
    last_name = db.Column(db.String, index=True, nullable=False)
    identification_filename = db.Column(db.String, index=True, nullable=True)
    identification_binary = db.Column(LargeBinary)
    proof_of_address_filename = db.Column(db.String, index=True, nullable=True)
    proof_of_address_binary = db.Column(LargeBinary)
    civility = db.Column(db.String, index=True, nullable=False)
    street = db.Column(db.String, index=True, nullable=False)
    zip = db.Column(db.String, index=True, nullable=False)
    city = db.Column(db.String, index=True, nullable=False)
    country = db.Column(CountryType, index=True, nullable=True)
    credit = db.Column(db.Float, index=True, nullable=True)
    credit_currency = db.Column(CurrencyType, index=True, nullable=True)
    firebase_id = db.Column(db.String(200), index=True, unique=True)

    # Relationships
    prepaid_account = relationship('PrepaidAccount', back_populates="user")
    phone_number_owner_user = relationship('PhoneNumberOwnerUser',
                                           back_populates="user")
    phone_number_2 = relationship('PhoneNumber', back_populates="user")
    company_user = relationship('CompanyUser', back_populates="user", uselist=False)
    subscription_company = relationship('SubscriptionCompany', back_populates="user")
    subscription_user = relationship('SubscriptionUser', foreign_keys='SubscriptionUser.user_id', back_populates="user")
    subscription_user_assigned = relationship('SubscriptionUser', foreign_keys='SubscriptionUser.user_id_assigned',
                                              back_populates="user_assigned")
    transaction = relationship('Transaction', back_populates="user")
    transaction_user = relationship('TransactionUser', back_populates="user")
    phone_number_transaction_user = relationship('PhoneNumberTransactionUser', back_populates="user")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        binary_identification = ""
        binary_proof_of_address = ""

        if self.identification_binary is not None:
            binary_identification = b64encode(self.identification_binary)

        if self.proof_of_address_binary is not None:
            binary_proof_of_address = b64encode(self.proof_of_address_binary)

        return {
            'id': self.id,
            'email': self.email,
            'phone_number': str(self.phone_number),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'identification_filename': self.identification_filename,
            'identification_binary': binary_identification,
            'proof_of_address_filename': self.proof_of_address_filename,
            'proof_of_address_binary': binary_proof_of_address,
            'civility': self.civility,
            'street': self.street,
            'zip': self.zip,
            'city': self.city,
            'country': str(self.country),
            'credit': self.credit,
            'credit_currency': str(self.credit_currency),
            'firebase_id': self.firebase_id
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_firebase_id(cls, firebase_id):
        return cls.query.filter_by(firebase_id=firebase_id).first()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()
