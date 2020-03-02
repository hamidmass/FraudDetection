from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy import ForeignKey


class PhoneNumberTransactionUser(db.Model):
    __tablename__ = 'phone_number_transaction_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(PhoneNumberType, index=True, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), index=True, nullable=True)
    start_time = db.Column(db.DateTime, index=True, nullable=True)
    end_time = db.Column(db.DateTime, index=True, nullable=True)

    # Relationships
    user = relationship('User', back_populates="phone_number_transaction_user")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'phone_number': str(self.phone_number),
            'user_id': self.user_id,
            'activated': self.activated,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_user_id(cls, user_id_2):
        return cls.query.filter_by(user_id=user_id_2).all()

    @classmethod
    def get_all_transactions(cls):
        return cls.query.all()

