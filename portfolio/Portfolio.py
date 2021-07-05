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

    def __add__(self, other):
        if other.currency != self.currency:
            raise ValueError

        return MoneyAmount(value=other.value + self.value, currency=self.currency)

    def __sub__(self, other):
        if other.currency != self.currency:
            raise ValueError

        return MoneyAmount(value=self.value - other.value, currency=self.currency)


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
    expected_yield: Optional[MoneyAmount]

    def average_buy(self):
        """Total average buy."""
        if self.average_price is None:
            return Decimal(0)

        value = self.average_price.value * self.balance

        return MoneyAmount(value=value, currency=self.average_price.currency)

    def market_price(self):
        if self.average_price is None:
            return Decimal(0)

        if self.expected_yield is None:
            return self.average_price

        yield_per_item = Decimal(self.expected_yield.value / self.balance)
        value = self.average_price.value + yield_per_item

        return MoneyAmount(value=value, currency=self.average_price.currency)

    def market_value(self):
        market_price = self.market_price()
        value = market_price.value * self.balance

        return MoneyAmount(value=value, currency=market_price.currency)

    def change_percent(self):
        if self.average_price is None:
            return Decimal(0)

        market_price = self.market_price()

        return (market_price.value * 100 / self.average_price.value - 100).quantize(Decimal('.01'))

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
    market_rates: {} = {}

    def pay_in_operations(self) -> [Operation]:
        def filter_pay_in(operation):
            return operation.operation_type == 'PayIn'

        return list(filter(filter_pay_in, self.operations))

    def total_pay_in(self):
        pay_in_operations = self.pay_in_operations()

        result = MoneyAmount(value=Decimal(0), currency='RUB')

        for operation in pay_in_operations:
            result += self.convert(MoneyAmount(value=operation.payment, currency=operation.currency), 'RUB')

        return result

    def pay_out_operations(self) -> [Operation]:
        def filter_pay_out(operation):
            return operation.operation_type == 'PayOut'

        return list(filter(filter_pay_out, self.operations))

    def total_pay_out(self):
        operations = self.pay_out_operations()

        result = MoneyAmount(value=Decimal(0), currency='RUB')

        for operation in operations:
            result += self.convert(MoneyAmount(value=operation.payment, currency=operation.currency), 'RUB')

        return result

    def adjusted_pay_in(self) -> MoneyAmount:
        pay_in = self.total_pay_in()
        pay_out = self.total_pay_out()

        # sum because pay_out is negative
        return pay_in + pay_out

    def buy_operations(self) -> [Operation]:
        def filter_buy(operation):
            is_buy_operation = (operation.operation_type == 'Buy') or (operation.operation_type == 'BuyCard')
            is_zero_operation = operation.payment == 0

            return is_buy_operation and not is_zero_operation

        return list(filter(filter_buy, self.operations))

    def buy_total(self) -> MoneyAmount:
        operations = self.buy_operations()

        result = MoneyAmount(value=Decimal(0), currency='RUB')

        for operation in operations:
            result += self.convert(MoneyAmount(value=operation.payment, currency=operation.currency), 'RUB')

        return result

    def sell_operations(self) -> [Operation]:
        def filter_sell(operation):
            is_sell_operation = operation.operation_type == 'Sell'
            is_zero_operation = operation.payment == 0

            return is_sell_operation and not is_zero_operation

        return list(filter(filter_sell, self.operations))

    def sell_total(self):
        operations = self.sell_operations()

        result = MoneyAmount(value=Decimal(0), currency='RUB')

        for operation in operations:
            result += self.convert(MoneyAmount(value=operation.payment, currency=operation.currency), 'RUB')

        return result

    def coupons(self) -> [Operation]:
        def filter_coupon(operation):
            return operation.operation_type == 'Coupon'

        return list(filter(filter_coupon, self.operations))

    def coupons_total(self):
        operations = self.coupons()

        result = MoneyAmount(value=Decimal(0), currency='RUB')

        for operation in operations:
            result += self.convert(MoneyAmount(value=operation.payment, currency=operation.currency), 'RUB')

        return result

    def dividends(self) -> [Operation]:
        def filter_dividends(operation):
            return operation.operation_type == 'Dividend'

        return list(filter(filter_dividends, self.operations))

    def dividends_total(self):
        operations = self.dividends()

        result = MoneyAmount(value=Decimal(0), currency='RUB')

        for operation in operations:
            result += self.convert(MoneyAmount(value=operation.payment, currency=operation.currency), 'RUB')

        return result

    def income_total(self):
        coupons = self.coupons_total()
        dividends = self.dividends_total()

        return coupons + dividends

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

    def tax_common(self) -> [Operation]:
        def filter_tax_common(operation):
            return operation.operation_type == 'Tax'

        return list(filter(filter_tax_common, self.operations))

    def tax_dividend(self) -> [Operation]:
        def filter_tax_dividend(operation):
            return operation.operation_type == 'TaxDividend'

        return list(filter(filter_tax_dividend, self.operations))

    def tax_coupon(self) -> [Operation]:
        def filter_tax_coupon(operation):
            return operation.operation_type == 'TaxCoupon'

        return list(filter(filter_tax_coupon, self.operations))

    def tax_lucre(self) -> [Operation]:
        def filter_tax_lucre(operation):
            return operation.operation_type == 'TaxLucre'

        return list(filter(filter_tax_lucre, self.operations))

    def tax_back(self) -> [Operation]:
        def filter_tax_back(operation):
            return operation.operation_type == 'TaxBack'

        return list(filter(filter_tax_back, self.operations))

    def all_portfolio_currencies(self) -> set[str]:
        result = set()

        for position in self.positions:
            if position.average_price is None:
                continue

            currency = position.average_price.currency
            result.add(currency)

        return result

    def convert(self, money_amount, target_currency):
        price = self.market_rates[money_amount.currency]
        value = money_amount.value * price

        return MoneyAmount(value=value, currency=target_currency)
