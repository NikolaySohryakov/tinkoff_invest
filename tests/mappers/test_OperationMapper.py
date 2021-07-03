import unittest
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from mappers import OperationMapper


class OperationMapperTests(unittest.TestCase):
    def setUp(self) -> None:
        currency = Mock()
        currency.value = 'USD'

        self.operation = Mock()
        self.operation.id = 'id'
        self.operation.figi = 'figi'
        self.operation.date = datetime.now()
        self.operation.currency = currency
        self.operation.payment = Decimal('100')

    def test_map(self):
        result = OperationMapper.map(self.operation)

        self.assertEqual(result.id, self.operation.id)
        self.assertEqual(result.figi, self.operation.figi)
        self.assertEqual(result.date, self.operation.date)
        self.assertEqual(result.currency, 'USD')
        self.assertEqual(result.payment, Decimal('100'))


if __name__ == '__main__':
    unittest.main()
