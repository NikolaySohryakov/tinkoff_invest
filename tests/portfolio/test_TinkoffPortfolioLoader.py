from unittest.mock import Mock
from datetime import date
import unittest

from portfolio import TinkoffPortfolioLoader


class TinkoffPortfolioLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        position_mock = Mock()
        position_mock.figi = 'figi'
        position_mock.name = 'name'
        position_mock.balance = 10.1
        position_mock.ticker = None

        # get_portfolio

        self.get_portfolio_payload_positions = [
                position_mock,
                position_mock
            ]

        get_portfolio_response_attrs = {
            'status': 'Ok',
            'payload.positions': self.get_portfolio_payload_positions
        }
        self.get_portfolio_response = Mock()
        self.get_portfolio_response.configure_mock(**get_portfolio_response_attrs)

        # get_operations

        self.get_operations_payload_operations = [
            Mock(),
            Mock()
        ]

        get_operations_response_attrs = {
            'status': 'Ok',
            'payload.operations': self.get_operations_payload_operations
        }
        self.get_operations_response = Mock()
        self.get_operations_response.configure_mock(**get_operations_response_attrs)

        # client

        self.client = Mock()
        self.client.get_portfolio.return_value = self.get_portfolio_response
        self.client.get_operations.return_value = self.get_operations_response

        self.loader = TinkoffPortfolioLoader(client=self.client, start_date=date(year=2021, month=3, day=3))

    def test_load(self):
        portfolio = self.loader.load()

        self.assertEqual(len(portfolio.positions), len(self.get_portfolio_payload_positions))


if __name__ == '__main__':
    unittest.main()
