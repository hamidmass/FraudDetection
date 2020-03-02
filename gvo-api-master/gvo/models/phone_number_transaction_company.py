from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy import ForeignKey


class PhoneNumberTransactionCompany(db.Model):
    __tablename__ = 'phone_number_transaction_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(PhoneNumberType, index=True, nullable=True)
    company_id = db.Column(db.Integer, ForeignKey('company.id'), index=True, nullable=True)
    start_time = db.Column(db.DateTime, index=True, nullable=True)
    end_time = db.Column(db.DateTime, index=True, nullable=True)

    # Relationships
    company = relationship('Company', back_populates="phone_number_transaction_company")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'phone_number': str(self.phone_number),
            'company_id': self.company_id,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_company_id(cls, company_id_2):
        return cls.query.filter_by(company_id=company_id_2).all()

    @classmethod
    def get_all_transactions(cls):
        return cls.query.all()


