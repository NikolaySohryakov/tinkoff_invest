from datetime import date
from datetime import time
from datetime import datetime

from mappers import PortfolioPositionMapper
from portfolio import Portfolio
from tinvest import SyncClient as TInvestClient


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

        return portfolio

    def __load_positions(self, portfolio):
        portfolio_dto = self.client.get_portfolio()

        assert portfolio_dto.status == 'Ok'

        portfolio_positions = list(map(PortfolioPositionMapper.map, portfolio_dto.payload.positions))
        portfolio.positions = portfolio_positions

    def __load_operations(self, portfolio):
        operations_dto = self.client.get_operations(from_=self.start_datetime, to=self.end_datetime)
        print(operations_dto)