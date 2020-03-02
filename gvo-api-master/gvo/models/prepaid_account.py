from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy import ForeignKey
from sqlalchemy_utils import CurrencyType


class PrepaidAccount(db.Model):
    __tablename__ = 'prepaid_account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    credit = db.Column(db.Float, index=True, nullable=False)
    credit_currency = db.Column(CurrencyType, unique=True, index=True, nullable=False)
    activated = db.Column(db.Boolean, index=True, nullable=False)
    time_activated_epoch = db.Column(db.DateTime, index=True, nullable=False)
    user_id_assigned = db.Column(db.Integer, ForeignKey('user.id'), index=True, nullable=True)

    # Relationships
    user = relationship('User', back_populates="prepaid_account")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'credit': self.credit,
            'credit_currency': self.credit_currency,
            'activated': self.activated,
            'time_activated_epoch': str(self.time_activated_epoch),
            'user_id_assigned': self.user_id_assigned
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def get_all_prepaid_accounts(cls):
        return cls.query.all()
