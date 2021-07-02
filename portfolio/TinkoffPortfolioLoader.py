from datetime import date
from dataclasses import dataclass

from mappers import PortfolioPositionMapper
from portfolio import Portfolio
from tinvest import SyncClient as TInvestClient


class TinkoffPortfolioLoader:
    config: TInvestClient
    start_at: date

    def __init__(self, client: TInvestClient, start_at: date):
        self.client = client
        self.start_at = start_at

    def load(self) -> Portfolio:
        portfolio_dto = self.client.get_portfolio()

        assert portfolio_dto.status == 'Ok'

        portfolio_positions = list(map(PortfolioPositionMapper.map, portfolio_dto.payload.positions))
        portfolio = Portfolio(positions=portfolio_positions)

        return portfolio
