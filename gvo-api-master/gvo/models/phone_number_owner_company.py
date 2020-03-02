from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy import ForeignKey


class PhoneNumberOwnerCompany(db.Model):
    __tablename__ = 'phone_number_owner_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, ForeignKey('company.id'), index=True, nullable=False)
    phone_number_id = db.Column(db.Integer, ForeignKey('phone_number.id'), index=True, nullable=False)

    # Relationships
    company = relationship('Company', back_populates="phone_number_owner_company")
    phone_number = relationship('PhoneNumber', back_populates="phone_number_owner_company")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'phone_number_id': self.phone_number_id
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_company_id(cls, company_id_2):
        return cls.query.filter_by(company_id=company_id_2).all()

    @classmethod
    def get_all_phone_owners(cls):
        return cls.query.all()
