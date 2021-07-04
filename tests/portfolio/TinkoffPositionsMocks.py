from decimal import Decimal
from unittest.mock import Mock


def __average_position_price(value, currency):
    mock = Mock()
    mock.value = Decimal(value)
    mock.currency.value = currency

    return mock


positions = [
    Mock(
        average_position_price=__average_position_price('10', 'USD')
    ),
    Mock(
        average_position_price=__average_position_price('12', 'RUB')
    ),
    Mock(
        average_position_price=__average_position_price('123', 'EUR')
    )
]