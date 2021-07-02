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

        self.payload_positions = [
                position_mock,
                position_mock
            ]

        response_mock_attrs = {
            'status': 'Ok',
            'payload.positions': self.payload_positions
        }
        self.response_mock = Mock()
        self.response_mock.configure_mock(**response_mock_attrs)

        self.client = Mock()
        self.client.get_portfolio.return_value = self.response_mock

        self.loader = TinkoffPortfolioLoader(client=self.client, start_at=date(year=2021, month=3, day=3))

    def test_load(self):
        portfolio = self.loader.load()

        self.assertEqual(len(portfolio.positions), len(self.payload_positions))


if __name__ == '__main__':
    unittest.main()
