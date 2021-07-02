import unittest
from decimal import Decimal

from portfolio import Portfolio
from portfolio import PortfolioPosition
from portfolio.Portfolio import MoneyAmount


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
        self.portfolio = Portfolio(
            positions=positions
        )

    def test_average(self):
        average = self.portfolio.average()

        self.assertEqual(average, Decimal('67.475'))


if __name__ == '__main__':
    unittest.main()
