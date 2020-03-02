from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy import ForeignKey


class SubscriptionCompany(db.Model):
    __tablename__ = 'subscription_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name_enum = db.Column(db.Integer, index=True, nullable=False)
    company_id = db.Column(db.Integer,  ForeignKey('company.id'), unique=True, index=True, nullable=False)
    user_id_assigned = db.Column(db.Integer, ForeignKey('user.id'), unique=True, index=True, nullable=True)
    mail = db.Column(db.String, unique=True, index=True, nullable=True)
    auto_renewal = db.Column(db.Boolean, unique=True, index=True, nullable=False)

    # Relationships
    user = relationship('User', back_populates="subscription_company")
    company = relationship('Company', back_populates="subscription_company")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'service_name_enum': self.service_name_enum,
            'company_id': self.company_id,
            'user_id_assigned': self.user_id_assigned,
            'mail': self.mail,
            'auto_renewal': self.auto_renewal
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_company_id(cls, company_id_2):
        return cls.query.filter_by(company_id=company_id_2).all()

    @classmethod
    def get_all_subscriptions(cls):
        return cls.query.all()
