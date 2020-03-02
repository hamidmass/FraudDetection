from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy import ForeignKey


class CompanyUser(db.Model):
    __tablename__ = 'company_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, ForeignKey('company.id'), index=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), index=True, nullable=False)

    # Relationships
    user = relationship('User', back_populates="company_user")
    company = relationship('Company', back_populates="company_user")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'user_id': self.user_id
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def get_all_company_users(cls, company_id_2):
        return cls.query.filter_by(company_id=company_id_2).all()
