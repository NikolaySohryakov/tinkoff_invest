from datetime import date
from datetime import time
from datetime import datetime

import mappers
from portfolio import Portfolio
from tinvest import SyncClient as TInvestClient


currencies_figi = {
    'USD': 'BBG0013HGFT4',
    'EUR': 'BBG0013HJJ31'
}


class TinkoffPortfolioLoader:
    config: TInvestClient

    def __init__(self, client: TInvestClient, start_date: date):
        self.client = client
        self.start_datetime = datetime.combine(date=start_date, time=time(hour=0, minute=0, second=0))
        self.end_datetime = datetime.now()

    def load(self) -> Portfolio:
        portfolio = Portfolio()

        self.__load_positions(portfolio)
        self.__load_operations(portfolio)
        self.__load_market_exchange_rates(portfolio)

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

                portfolio.currency_prices[currency] = last_price
            except KeyError:
                print('Skipping currency:' + currency)
                pass
