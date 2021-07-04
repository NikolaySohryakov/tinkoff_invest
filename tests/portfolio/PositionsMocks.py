from decimal import Decimal
from unittest.mock import Mock

from portfolio import MoneyAmount

positions = [
    Mock(
        average_price=MoneyAmount(value=Decimal('123.7'), currency='RUB')
    ),
    Mock(
        average_price=MoneyAmount(value=Decimal('10'), currency='USD')
    ),
    Mock(
        average_price=None
    )
]