from datetime import datetime
from typing import List

from app.models.base_donation import BaseDonation


def investment(
    target: BaseDonation,
    sources: List[BaseDonation]
) -> List[BaseDonation]:
    """
    Инвестирует в целевой донат из списка исходных донатов.
    """
    modified = []

    for source in sources:
        to_invest = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += to_invest
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
        modified.append(source)
        if target.fully_invested:
            break
    return modified
