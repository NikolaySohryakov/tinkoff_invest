from decimal import Decimal
from unittest.mock import Mock

from portfolio import MoneyAmount, PortfolioPosition

positions = [
    PortfolioPosition(
        figi='figi1',
        isin='isin1',
        name='nam1',
        ticker='ticker1',
        balance=Decimal(10),
        lots=1,
        average_price=MoneyAmount(value=Decimal('123.7'), currency='RUB'),
        average_price_no_nkd=MoneyAmount(value=Decimal('123.7'), currency='RUB'),
        expected_yield=MoneyAmount(value=Decimal('140'), currency='RUB'),
    ),
    PortfolioPosition(
        figi='figi2',
        isin='isin2',
        name='nam2',
        ticker='ticker2',
        balance=Decimal(100),
        lots=2,
        average_price=MoneyAmount(value=Decimal('10'), currency='RUB'),
        average_price_no_nkd=MoneyAmount(value=Decimal('10'), currency='RUB'),
        expected_yield=MoneyAmount(value=Decimal('14'), currency='RUB'),
    ),
    PortfolioPosition(
        figi='figi3',
        isin='isin3',
        name='nam3',
        ticker='ticker3',
        balance=Decimal(5),
        lots=5,
        average_price=MoneyAmount(value=Decimal('30'), currency='USD'),
        average_price_no_nkd=MoneyAmount(value=Decimal('10'), currency='USD'),
        expected_yield=MoneyAmount(value=Decimal('14'), currency='USD'),
    )
]