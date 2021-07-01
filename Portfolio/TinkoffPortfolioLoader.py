from datetime import date
from dataclasses import dataclass

from Mappers.PortfolioPositionMapper import PortfolioPositionMapper
from Portfolio.Portfolio import Portfolio
from tinvest import SyncClient as TInvestClient


@dataclass
class TinkoffConfig:
    production_token: str
    sandbox_token: str
    use_sandbox: bool

    def token(self):
        return self.sandbox_token if self.use_sandbox else self.production_token


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
