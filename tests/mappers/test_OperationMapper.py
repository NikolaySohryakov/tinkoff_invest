import unittest
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from mappers import OperationMapper
from portfolio import MoneyAmount


class OperationMapperTests(unittest.TestCase):
    def setUp(self) -> None:
        currency = Mock()
        currency.value = 'USD'

        operation_type = Mock()
        operation_type.value = 'operation_type'

        status = Mock()
        status.value = 'status'

        self.operation = Mock()
        self.operation.id = 'id'
        self.operation.figi = 'figi'
        self.operation.date = datetime.now()
        self.operation.currency = currency
        self.operation.payment = Decimal('100')
        self.operation.commission = MoneyAmount(value=Decimal('10'), currency='USD')
        self.operation.operation_type = operation_type
        self.operation.price = Decimal('100')
        self.operation.quantity = 10
        self.operation.status = status

    def test_map(self):
        result = OperationMapper.map(self.operation)

        self.assertEqual(result.id, self.operation.id)
        self.assertEqual(result.figi, self.operation.figi)
        self.assertEqual(result.date, self.operation.date)
        self.assertEqual(result.currency, 'USD')
        self.assertEqual(result.payment, Decimal('100'))
        self.assertEqual(result.commission.value, Decimal('10'))
        self.assertEqual(result.commission.currency, 'USD')
        self.assertEqual(result.operation_type, 'operation_type')
        self.assertEqual(result.price, Decimal('100'))
        self.assertEqual(result.quantity, 10)
        self.assertEqual(result.status, 'status')


if __name__ == '__main__':
    unittest.main()
