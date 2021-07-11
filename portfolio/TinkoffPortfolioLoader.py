import time as _time
from datetime import date
from datetime import time
from datetime import datetime
from decimal import Decimal

import mappers
from ExchangeRatesProvider import ExchangeRatesProvider
from portfolio import Portfolio, PortfolioPosition, Operation
from tinvest import SyncClient as TInvestClient, CurrencyPosition, Currency

currencies_figi = {
    'USD': 'BBG0013HGFT4',
    'EUR': 'BBG0013HJJ31'
}


class TinkoffPortfolioLoader:
    config: TInvestClient

    def __init__(self, client: TInvestClient, exchange_rates_provider: ExchangeRatesProvider, start_date: date):
        self.client = client
        self.exchange_rates_provider = exchange_rates_provider
        self.start_datetime = datetime.combine(date=start_date, time=time(hour=0, minute=0, second=0))
        self.end_datetime = datetime.now()

    def load(self) -> Portfolio:
        portfolio = Portfolio()

        self.__load_positions(portfolio)
        self.__load_operations(portfolio)
        self.__load_market_exchange_rates(portfolio)
        self.__load_rub(portfolio)

        self.__load_cb_rf_rates(portfolio)

        return portfolio

    def __load_positions(self, portfolio):
        portfolio_dto = self.client.get_portfolio()

        assert portfolio_dto.status == 'Ok'

        portfolio_positions = list(map(mappers.PortfolioPositionMapper.map, portfolio_dto.payload.positions))
        portfolio.positions = portfolio_positions

    def __load_operations(self, portfolio):
        operations_dto = self.client.get_operations(from_=self.start_datetime, to=self.end_datetime)

        assert operations_dto.status == 'Ok'

        operations = list(map(mappers.OperationMapper.map, operations_dto.payload.operations))
        portfolio.operations = operations

    def __load_market_exchange_rates(self, portfolio):
        currencies = portfolio.all_portfolio_currencies()

        for currency in currencies:
            try:
                figi = currencies_figi[currency]

                orderbook = self.client.get_market_orderbook(figi, 20)
                last_price = orderbook.payload.last_price

                portfolio.market_rates[currency] = last_price
            except KeyError:
                print('Skipping currency:' + currency)
                pass

        portfolio.market_rates['RUB'] = Decimal('1')

    def __load_rub(self, portfolio):
        currencies = self.client.get_portfolio_currencies()

        def rub_filter(position: CurrencyPosition):
            return position.currency == Currency.rub

        currency_position = list(filter(rub_filter, currencies.payload.currencies))[0]

        portfolio_position = PortfolioPosition.fake_rub(currency_position.balance)

        portfolio.positions.append(portfolio_position)

    def __load_cb_rf_rates(self, portfolio):
        def currency_filter(operation: Operation):
            return operation.currency != 'RUB'

        def date_map(operation: Operation):
            return operation.date.date()

        operations = list(filter(currency_filter, portfolio.operations))
        dates = set(map(date_map, operations))

        result = {}

        for operation_date in dates:
            result[operation_date] = self.exchange_rates_provider.rates(on_date=operation_date)
            _time.sleep(0.1)

        portfolio.exchange_rates = result
