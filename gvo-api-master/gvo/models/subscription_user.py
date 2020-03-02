from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy import ForeignKey, Enum
from gvo.models.service_name_enum import ServiceNameEnum


class SubscriptionUser(db.Model):
    __tablename__ = 'subscription_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name_enum = db.Column(Enum(ServiceNameEnum), index=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), unique=True, index=True, nullable=False)
    user_id_assigned = db.Column(db.Integer, ForeignKey('user.id'), unique=True, index=True, nullable=True)
    mail = db.Column(db.String, unique=True, index=True, nullable=True)
    auto_renewal = db.Column(db.Boolean, unique=True, index=True, nullable=False)

    # Relationships
    user = relationship('User', foreign_keys=user_id, back_populates="subscription_user")
    user_assigned = relationship('User', foreign_keys=user_id_assigned, back_populates="subscription_user_assigned")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'service_name_enum': self.service_name_enum,
            'user_id': self.user_id,
            'user_id_assigned': self.user_id_assigned,
            'mail': self.mail,
            'auto_renewal': self.auto_renewal
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_user_id(cls, user_id_2):
        return cls.query.filter_by(user_id=user_id_2).all()

    @classmethod
    def get_all_subscriptions(cls):
        return cls.query.all()
