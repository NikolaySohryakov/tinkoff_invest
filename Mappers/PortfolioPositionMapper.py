from tinvest import PortfolioPosition as TinkoffPortfolioPosition
from Portfolio.Portfolio import PortfolioPosition


class PortfolioPositionMapper:
    @staticmethod
    def map(tinkoff_portfolio_position: TinkoffPortfolioPosition) -> PortfolioPosition:
        return PortfolioPosition(figi=tinkoff_portfolio_position.figi,
                                 name=tinkoff_portfolio_position.name,
                                 ticker=tinkoff_portfolio_position.ticker,
                                 balance=tinkoff_portfolio_position.balance,
                                 )
