import unittest
from decimal import Decimal
from unittest.mock import Mock

from portfolio import Portfolio, MoneyAmount
from tests.portfolio import OperationsMocks, PositionsMocks


class PortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.portfolio = Portfolio()
        self.portfolio.positions = PositionsMocks.positions
        self.portfolio.operations = OperationsMocks.operations
        self.portfolio.market_rates = {
            'USD': Decimal('73.3'),
            'RUB': Decimal('1')
        }

    def test_pay_in_operations(self):
        operations = self.portfolio.pay_in_operations()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'PayIn')

    def test_total_pay_in(self):
        result = self.portfolio.total_pay_in()

        self.assertEqual(result.currency,  'RUB')
        self.assertEqual(result.value, Decimal('833'))

    def test_pay_out_operations(self):
        operations = self.portfolio.pay_out_operations()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'PayOut')

    def test_total_pay_out(self):
        result = self.portfolio.total_pay_out()
        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-466.5'))

    def test_adjusted_pay_in(self):
        result = self.portfolio.adjusted_pay_in()
        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('366.5'))

    def test_buy_operations(self):
        zero_buy = Mock(
            operation_type='Buy',
            payment=Decimal('0')
        )
        zero_buy_card = Mock(
            operation_type='BuyCard',
            payment=Decimal('0')
        )
        self.portfolio.operations.append(zero_buy)
        self.portfolio.operations.append(zero_buy_card)

        operations = self.portfolio.buy_operations()

        self.assertEqual(len(operations), 3)

        for operation in operations:
            self.assertNotEqual(operation.payment, 0)

    def test_buy_total(self):
        result = self.portfolio.buy_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-7503.3'))

    def test_sell_operations(self):
        zero_sell = Mock(
            operation_type='Sell',
            payment=Decimal('0')
        )
        self.portfolio.operations.append(zero_sell)

        operations = self.portfolio.sell_operations()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'Sell')

        for operation in operations:
            self.assertNotEqual(operation.payment, 0)

    def test_sell_total(self):
        result = self.portfolio.sell_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('7340'))

    def test_coupons(self):
        operations = self.portfolio.coupons()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'Coupon')

    def test_coupons_total(self):
        result = self.portfolio.coupons_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('1842.5'))

    def test_dividends(self):
        operations = self.portfolio.dividends()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'Dividend')

    def test_dividends_total(self):
        result = self.portfolio.dividends_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('1834.5'))

    def test_income_total(self):
        result = self.portfolio.income_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('3677.0'))

    def test_broker_commissions(self):
        operations = self.portfolio.broker_commissions()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'BrokerCommission')

    def test_total_broker_commissions(self):
        result = self.portfolio.total_broker_commissions()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-91.875'))

    def test_exchange_commissions(self):
        operations = self.portfolio.exchange_commissions()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'ExchangeCommission')

    def test_total_exchange_commissions(self):
        result = self.portfolio.total_exchange_commissions()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-20.575'))

    def test_service_commissions(self):
        operations = self.portfolio.service_commissions()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'ServiceCommission')

    def test_total_service_commissions(self):
        result = self.portfolio.total_service_commissions()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-30.063'))

    def test_margin_commissions(self):
        operations = self.portfolio.margin_commissions()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'MarginCommission')

    def test_total_margin_commissions(self):
        result = self.portfolio.total_margin_commissions()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-15.703'))

    def test_other_commissions(self):
        operations = self.portfolio.other_commissions()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'OtherCommission')

    def test_total_other_commissions(self):
        result = self.portfolio.total_other_commissions()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-10.473'))

    def test_total_all_commissions(self):
        result = self.portfolio.total_all_commissions()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-168.689'))

    def test_tax_common(self):
        operations = self.portfolio.tax_common()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'Tax')

    def test_tax_common_total(self):
        result = self.portfolio.tax_common_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-368.5'))

    def test_tax_dividend(self):
        operations = self.portfolio.tax_dividend()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'TaxDividend')

    def test_tax_dividend_total(self):
        result = self.portfolio.tax_dividend_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-242.2'))

    def test_tax_coupon(self):
        operations = self.portfolio.tax_coupon()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'TaxCoupon')

    def test_tax_coupon_total(self):
        result = self.portfolio.tax_coupon_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-24.29'))

    def test_tax_lucre(self):
        operations = self.portfolio.tax_lucre()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'TaxLucre')

    def test_tax_lucre_total(self):
        result = self.portfolio.tax_lucre_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-26.86'))

    def test_tax_back(self):
        operations = self.portfolio.tax_back()

        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0].operation_type, 'TaxBack')

    def test_tax_back_total(self):
        result = self.portfolio.tax_back_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-466.1'))

    def test_tax_total(self):
        result = self.portfolio.tax_total()

        self.assertEqual(result.currency, 'RUB')
        self.assertEqual(result.value, Decimal('-1127.95'))

    def test_all_portfolio_currencies(self):
        currencies = self.portfolio.all_portfolio_currencies()

        self.assertEqual({'USD', 'RUB'}, currencies)

    def test_convert_currency_usd_to_rub(self):
        money_amount = MoneyAmount(value=Decimal(10), currency='USD')
        self.portfolio.market_rates = {'USD': Decimal('73.3')}
        result = self.portfolio.convert(money_amount, 'RUB')

        self.assertEqual('RUB', result.currency)
        self.assertEqual(Decimal(733), result.value)

    def test_clean_portfolio(self):
        result = self.portfolio.market_value()

        self.assertEqual('RUB', result.currency)
        self.assertEqual(Decimal('14412.20'), result.value)


if __name__ == '__main__':
    unittest.main()
