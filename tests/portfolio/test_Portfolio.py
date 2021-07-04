import unittest
from decimal import Decimal
from unittest.mock import Mock

from portfolio import Portfolio
from portfolio import PortfolioPosition
from portfolio.Portfolio import MoneyAmount
from tests.portfolio import OperationsMocks


class PortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        positions = [
            PortfolioPosition(figi='',
                              isin='',
                              name='',
                              ticker=None,
                              balance=Decimal('1'),
                              lots=10,
                              average_price=MoneyAmount(value=Decimal('123.7'), currency='RUB'),
                              average_price_no_nkd=MoneyAmount(value=Decimal('123.7'), currency='RUB')
                              ),

            PortfolioPosition(figi='',
                              isin='',
                              name='',
                              ticker=None,
                              balance=Decimal('11'),
                              lots=10,
                              average_price=MoneyAmount(value=Decimal('11.25'), currency='RUB'),
                              average_price_no_nkd=MoneyAmount(value=Decimal('11.25'), currency='RUB')
                              ),
        ]

        self.portfolio = Portfolio()
        self.portfolio.positions = positions
        self.portfolio.operations = OperationsMocks.operations

    def test_pay_in_operations(self):
        operations = self.portfolio.pay_in_operations()

        self.assertEqual(len(operations), 1)

    def test_pay_out_operations(self):
        operations = self.portfolio.pay_out_operations()

        self.assertEqual(len(operations), 1)


if __name__ == '__main__':
    unittest.main()
