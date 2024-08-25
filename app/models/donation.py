from sqlalchemy import Column, ForeignKey, Integer, String

from .base_donation import BaseDonation


class Donation(BaseDonation):
    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String, nullable=True)

    def __repr__(self):
        return (
            f'Пожертвование на сумму {self.full_amount}, '
            f'из них потрачено {self.invested_amount}'
        )
