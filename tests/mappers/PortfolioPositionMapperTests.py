from decimal import Decimal
from unittest.mock import Mock
import unittest

from mappers import PortfolioPositionMapper


class PortfolioPositionMapperTests(unittest.TestCase):
    def test_map(self):
        currency_usd = Mock()
        currency_usd.value = 'USD'

        position_price = Mock()
        position_price.value = Decimal(10)
        position_price.currency = currency_usd

        portfolio_position = Mock()
        portfolio_position.figi = 'figi'
        portfolio_position.name = 'name'
        portfolio_position.ticker = 'ticker'
        portfolio_position.balance = 10.1
        portfolio_position.average_position_price = position_price
        portfolio_position.average_position_price_no_nkd = position_price

        result = PortfolioPositionMapper.map(portfolio_position)

        self.assertEqual(result.figi, portfolio_position.figi)
        self.assertEqual(result.name, portfolio_position.name)
        self.assertEqual(result.ticker, portfolio_position.ticker)
        self.assertEqual(result.balance, portfolio_position.balance)
        self.assertEqual(result.average_price.value, Decimal('10'))
        self.assertEqual(result.average_price.currency, 'USD')
        self.assertEqual(result.average_price_no_nkd.value, Decimal('10'))
        self.assertEqual(result.average_price_no_nkd.currency, 'USD')


if __name__ == '__main__':
    unittest.main()
