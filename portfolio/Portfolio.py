from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class MoneyAmount:
    value: Decimal
    _currency = None

    def __init__(self, value: Decimal, currency: str):
        self.value = value
        self._currency = currency

    @property
    def currency(self):
        """ISO 4217 currency code"""
        return self._currency.upper()


@dataclass
class PortfolioPosition:
    figi: str
    isin: Optional[str]
    name: str
    ticker: Optional[str]
    balance: Decimal  # lots * number of items per lot
    lots: int
    average_price: Optional[MoneyAmount]
    average_price_no_nkd: Optional[MoneyAmount]

    def __radd__(self, other):
        return other + self.average_price_no_nkd.value


@dataclass
class Operation:
    id: str
    figi: Optional[str]
    date: datetime
    currency: str  # ISO 4217 currency code
    payment: Decimal
    commission: Optional[MoneyAmount]
    operation_type: str
    price: Optional[Decimal]
    quantity: Optional[int]
    status: str


class Portfolio:
    positions: [PortfolioPosition] = []
    operations: [Operation] = []

    def pay_in_operations(self) -> [Operation]:
        def filter_pay_in(operation):
            return operation.operation_type == 'PayIn'

        return list(filter(filter_pay_in, self.operations))

    def pay_out_operations(self) -> [Operation]:
        def filter_pay_out(operation):
            return operation.operation_type == 'PayOut'

        return list(filter(filter_pay_out, self.operations))

    def buy_operations(self) -> [Operation]:
        def filter_buy(operation):
            is_buy_operation = (operation.operation_type == 'Buy') or (operation.operation_type == 'BuyCard')
            is_zero_operation = operation.payment == 0

            return is_buy_operation and not is_zero_operation

        return list(filter(filter_buy, self.operations))
