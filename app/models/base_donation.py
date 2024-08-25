from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BaseDonation(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            'full_amount >= 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_not_exceed_full'
        )
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f'полная сумма,={self.full_amount},'
            f'инвестированная сумма={self.invested_amount},'
        )
