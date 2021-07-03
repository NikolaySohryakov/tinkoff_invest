import unittest
from decimal import Decimal
from unittest.mock import Mock

from tinvest import MoneyAmount as TinkoffMoneyAmount
from tinvest import Currency

from mappers.MoneyAmountMapper import MoneyAmountMapper


class MyTestCase(unittest.TestCase):
    def test_map(self):
        money_amount = Mock()
        money_amount.currency = Currency('USD')
        money_amount.value = Decimal('100')

        mapped_money_amount = MoneyAmountMapper.map(money_amount)

        self.assertEqual(mapped_money_amount.value, Decimal('100'))
        self.assertEqual(mapped_money_amount.currency, 'USD')


if __name__ == '__main__':
    unittest.main()
