from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from gvo.app import db


class PhoneNumberOwnerUser(db.Model):
    __tablename__ = 'phone_number_owner_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), index=True, nullable=False)
    phone_number_id = db.Column(db.Integer, ForeignKey('phone_number.id'), index=True, nullable=False)

    # Relationships
    user = relationship('User', back_populates="phone_number_owner_user")
    phone_number = relationship('PhoneNumber', back_populates="phone_number_owner_user")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'phone_number_id': self.phone_number_id
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_user_id(cls, user_id_2):
        return cls.query.filter_by(user_id=user_id_2).all()

    @classmethod
    def get_all_phone_owners(cls):
        return cls.query.all()
