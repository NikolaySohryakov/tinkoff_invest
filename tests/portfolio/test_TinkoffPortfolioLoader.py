from decimal import Decimal
from unittest.mock import Mock
from datetime import date
import unittest

from portfolio import TinkoffPortfolioLoader
from tests.portfolio import TinkoffOperationsMocks, TinkoffPositionsMocks


class TinkoffPortfolioLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        # get_portfolio

        self.get_portfolio_payload_positions = TinkoffPositionsMocks.positions

        get_portfolio_response_attrs = {
            'status': 'Ok',
            'payload.positions': self.get_portfolio_payload_positions
        }
        self.get_portfolio_response = Mock()
        self.get_portfolio_response.configure_mock(**get_portfolio_response_attrs)

        # get_operations

        self.get_operations_payload_operations = TinkoffOperationsMocks.operations

        get_operations_response_attrs = {
            'status': 'Ok',
            'payload.operations': self.get_operations_payload_operations
        }
        self.get_operations_response = Mock()
        self.get_operations_response.configure_mock(**get_operations_response_attrs)

        # get_market_orderbook

        def get_market_orderbook_side_effect(figi, depth):
            result = Mock()
            result.payload = Mock()

            if figi == 'BBG0013HGFT4':
                result.payload.last_price = Decimal('73.2')
            else:
                result.payload.last_price = Decimal('80.0')

            return result

        # client

        self.client = Mock()
        self.client.get_portfolio.return_value = self.get_portfolio_response
        self.client.get_operations.return_value = self.get_operations_response
        self.client.get_market_orderbook.side_effect = get_market_orderbook_side_effect

        self.loader = TinkoffPortfolioLoader(client=self.client, start_date=date(year=2021, month=3, day=3))

    def test_load(self):
        portfolio = self.loader.load()

        self.assertEqual(len(portfolio.positions), len(self.get_portfolio_payload_positions))
        self.assertEqual(len(portfolio.operations), len(self.get_operations_payload_operations))
        self.assertEqual(2, self.client.get_market_orderbook.call_count)
        self.assertEqual(portfolio.market_rates, {
            'USD': Decimal('73.2'),
            'EUR': Decimal('80.0'),
            'RUB': Decimal(1)
        })


if __name__ == '__main__':
    unittest.main()
