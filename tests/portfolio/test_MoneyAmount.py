import unittest
from decimal import Decimal

from portfolio import MoneyAmount


class MyTestCase(unittest.TestCase):
    def test_currency_always_upper(self):
        money_amount = MoneyAmount(value=Decimal('10'), currency='usd')

        self.assertTrue(money_amount.currency.isupper())


if __name__ == '__main__':
    unittest.main()
