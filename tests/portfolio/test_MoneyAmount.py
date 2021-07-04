import unittest
from decimal import Decimal

from portfolio import MoneyAmount


class MoneyAmountTests(unittest.TestCase):
    def test_currency_always_upper(self):
        money_amount = MoneyAmount(value=Decimal('10'), currency='usd')

        self.assertTrue(money_amount.currency.isupper())

    def test_add(self):
        money_amount1 = MoneyAmount(value=Decimal('10'), currency='USD')
        money_amount2 = MoneyAmount(value=Decimal('20'), currency='USD')

        result = money_amount1 + money_amount2

        self.assertEqual(Decimal(30), result.value)
        self.assertEqual('USD', result.currency)

    def test_add_different_currencies(self):
        money_amount1 = MoneyAmount(value=Decimal('10'), currency='USD')
        money_amount2 = MoneyAmount(value=Decimal('20'), currency='RUB')

        with self.assertRaises(ValueError):
            result = money_amount1 + money_amount2


if __name__ == '__main__':
    unittest.main()
