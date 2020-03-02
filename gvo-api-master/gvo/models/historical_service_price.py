from sqlalchemy.orm import relationship
from sqlalchemy_utils import CountryType, CurrencyType
from gvo.app import db
from sqlalchemy import Enum
from gvo.models.service_name_enum import ServiceNameEnum


class HistoricalServicePrice(db.Model):
    __tablename__ = 'historical_service_price'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name_enum = db.Column(Enum(ServiceNameEnum), index=True, nullable=False)
    country = db.Column(CountryType, index=True, nullable=False)
    region = db.Column(db.String, index=True, nullable=False)
    time_epoch = db.Column(db.DateTime, index=True, nullable=False)
    price = db.Column(db.Float, index=True, nullable=False)
    currency = db.Column(CurrencyType, index=True, nullable=False)

    # Relationships
    transaction = relationship('Transaction', back_populates="historical_service_price")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'service_name_enum': str(self.service_name_enum),
            'country': str(self.country),
            'region': self.region,
            'time_epoch': str(self.time_epoch),
            'price': self.price,
            'currency': str(self.currency)
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def get_all_service_prices(cls):
        return cls.query.all()
