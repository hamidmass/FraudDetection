from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy import ForeignKey


class TransactionCompany(db.Model):
    __tablename__ = 'transaction_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, ForeignKey('company.id'), index=True, nullable=False)
    transaction_id = db.Column(db.Integer, ForeignKey('transaction.id'), index=True, nullable=False)

    # Relationships
    company = relationship('Company', back_populates="transaction_company")
    transaction = relationship('Transaction', back_populates="transaction_company")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'transaction_id': self.transaction_id
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_company_id(cls, company_id_2):
        return cls.query.filter_by(company_id=company_id_2).all()

    @classmethod
    def get_all_transactions_companies(cls):
        return cls.query.all()
