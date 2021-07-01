from unittest.mock import Mock
import unittest

from Mappers.PortfolioPositionMapper import PortfolioPositionMapper


class PortfolioPositionMapperTests(unittest.TestCase):
    def test_map(self):
        portfolio_position = Mock()
        portfolio_position.figi = 'figi'
        portfolio_position.name = 'name'
        portfolio_position.ticker = 'ticker'
        portfolio_position.balance = 10.1

        result = PortfolioPositionMapper.map(portfolio_position)

        self.assertEqual(result.figi, portfolio_position.figi)
        self.assertEqual(result.name, portfolio_position.name)
        self.assertEqual(result.ticker, portfolio_position.ticker)
        self.assertEqual(result.balance, portfolio_position.balance)


if __name__ == '__main__':
    unittest.main()
