from sqlalchemy.orm import relationship
from gvo.app import db
from sqlalchemy import ForeignKey


class TransactionUser(db.Model):
    __tablename__ = 'transaction_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), index=True, nullable=False)
    transaction_id = db.Column(db.Integer, ForeignKey('transaction.id'), index=True, nullable=False)

    # Relationships
    transaction = relationship('Transaction', back_populates="transaction_user")
    user = relationship('User', back_populates="transaction_user")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transaction_id': self.transaction_id
        }

    @classmethod
    def find_by_id(cls, id_2):
        return cls.query.filter_by(id=id_2).first()

    @classmethod
    def find_by_user_id(cls, user_id_2):
        return cls.query.filter_by(user_id=user_id_2).all()

    @classmethod
    def get_all_transactions_user(cls):
        return cls.query.all()
