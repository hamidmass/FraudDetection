from sqlalchemy.orm import relationship
from sqlalchemy_utils import CountryType
from gvo.app import db
from sqlalchemy import ForeignKey, Enum, DateTime
from gvo.models.service_name_enum import ServiceNameEnum


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name_enum = db.Column(Enum(ServiceNameEnum), index=True, nullable=False)
    user_id_assigned = db.Column(db.Integer, ForeignKey('user.id'), index=True, nullable=True)
    mail = db.Column(db.String, index=True, nullable=True)
    historical_service_price_id = db.Column(db.Integer, ForeignKey('historical_service_price.id'), index=True,
                                            nullable=False)
    country = db.Column(CountryType, index=True, nullable=False)
    region = db.Column(db.String, index=True, nullable=False)
    start_time = db.Column(DateTime, index=True, nullable=False)
    end_time = db.Column(DateTime, index=True, nullable=False)

    # Relationships
    user = relationship('User', back_populates="transaction")
    historical_service_price = relationship('HistoricalServicePrice', back_populates="transaction")
    transaction_company = relationship('TransactionCompany', back_populates="transaction", uselist=False)
    transaction_user = relationship('TransactionUser', back_populates="transaction", uselist=False)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'service_name_enum': str(self.service_name_enum),
            'user_id_assigned': self.user_id_assigned,
            'mail': self.mail,
            'historical_service_price_id': self.historical_service_price_id,
            'country': str(self.country),
            'region': self.region,
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
        }


    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_user_id_assigned(cls, user_id_assigned_2):
        return cls.query.filter_by(user_id_assigned=user_id_assigned_2).all()

    @classmethod
    def get_all_transactions(cls):
        return cls.query.all()


