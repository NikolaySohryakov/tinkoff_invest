import unittest
from decimal import Decimal

from Portfolio.Portfolio import Portfolio
from Portfolio.Portfolio import PortfolioPosition


class PortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        positions = [
            PortfolioPosition(figi='', name='', ticker=None, balance=Decimal('123.7')),
            PortfolioPosition(figi='', name='', ticker=None, balance=Decimal('11.25')),
        ]
        self.portfolio = Portfolio(
            positions=positions
        )

    def test_average(self):
        average = self.portfolio.average()

        self.assertEqual(average, Decimal('67.475'))


if __name__ == '__main__':
    unittest.main()
