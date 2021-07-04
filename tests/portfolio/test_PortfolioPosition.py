import unittest
from decimal import Decimal

from portfolio import PortfolioPosition, MoneyAmount


class PortfolioPositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.position = PortfolioPosition(
            figi='',
            isin='',
            name='',
            balance=Decimal(10),
            average_price=MoneyAmount(value=Decimal('20'), currency='USD'),
            average_price_no_nkd=None,
            ticker='',
            lots=1,
            expected_yield=MoneyAmount(value=Decimal('20'), currency='USD'),
        )

    def test_average_buy(self):
        self.position.average_price = MoneyAmount(value=Decimal('21.2'), currency='USD')
        result = self.position.average_buy()

        self.assertEqual(Decimal('212'), result.value)
        self.assertEqual('USD', result.currency)

    def test_market_price_positive(self):
        self.position.average_price = MoneyAmount(value=Decimal('553'), currency='RUB')
        self.position.expected_yield = MoneyAmount(value=Decimal('100'), currency='RUB')

        result = self.position.market_price()

        self.assertEqual(Decimal(563), result.value)
        self.assertEqual('RUB', result.currency)

    def test_market_price_negative(self):
        self.position.average_price = MoneyAmount(value=Decimal('553'), currency='RUB')
        self.position.expected_yield = MoneyAmount(value=Decimal('-15'), currency='RUB')

        result = self.position.market_price()

        self.assertEqual(Decimal(551.5), result.value)
        self.assertEqual('RUB', result.currency)

    def test_change_percent_positive(self):
        self.position.average_price = MoneyAmount(value=Decimal('71.61'), currency='RUB')
        self.position.expected_yield = MoneyAmount(value=Decimal('59.10'), currency='RUB')

        result = self.position.change_percent()

        self.assertEqual(Decimal('8.25'), result)

    def test_change_percent_negative(self):
        self.position.average_price = MoneyAmount(value=Decimal('71.61'), currency='RUB')
        self.position.expected_yield = MoneyAmount(value=Decimal('-59.10'), currency='RUB')

        result = self.position.change_percent()

        self.assertEqual(Decimal('-8.25'), result)

    def test_market_value(self):
        self.position.average_price = MoneyAmount(value=Decimal('71.61'), currency='RUB')
        self.position.expected_yield = MoneyAmount(value=Decimal('-59.10'), currency='RUB')

        result = self.position.market_value()

        self.assertEqual(Decimal('657'), result.value)
        self.assertEqual('RUB', result.currency)


if __name__ == '__main__':
    unittest.main()
