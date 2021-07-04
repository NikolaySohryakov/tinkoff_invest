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

    def sell_operations(self) -> [Operation]:
        def filter_sell(operation):
            is_sell_operation = operation.operation_type == 'Sell'
            is_zero_operation = operation.payment == 0

            return is_sell_operation and not is_zero_operation

        return list(filter(filter_sell, self.operations))

    def coupons(self) -> [Operation]:
        def filter_coupon(operation):
            return operation.operation_type == 'Coupon'

        return list(filter(filter_coupon, self.operations))

    def dividends(self) -> [Operation]:
        def filter_dividends(operation):
            return operation.operation_type == 'Dividend'

        return list(filter(filter_dividends, self.operations))

    def broker_commissions(self) -> [Operation]:
        def filter_broker_commissions(operation):
            return operation.operation_type == 'BrokerCommission'

        return list(filter(filter_broker_commissions, self.operations))

    def exchange_commissions(self) -> [Operation]:
        def filter_exchange_commissions(operation):
            return operation.operation_type == 'ExchangeCommission'

        return list(filter(filter_exchange_commissions, self.operations))

    def service_commissions(self) -> [Operation]:
        def filter_service_commissions(operation):
            return operation.operation_type == 'ServiceCommission'

        return list(filter(filter_service_commissions, self.operations))

    def margin_commissions(self) -> [Operation]:
        def filter_margin_commissions(operation):
            return operation.operation_type == 'MarginCommission'

        return list(filter(filter_margin_commissions, self.operations))

    def other_commissions(self) -> [Operation]:
        def filter_other_commissions(operation):
            return operation.operation_type == 'OtherCommission'

        return list(filter(filter_other_commissions, self.operations))
