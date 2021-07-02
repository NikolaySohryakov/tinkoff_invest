from tinvest import PortfolioPosition as TinkoffPortfolioPosition

from mappers.MoneyAmountMapper import MoneyAmountMapper
from portfolio import PortfolioPosition


class PortfolioPositionMapper:
    @staticmethod
    def map(tinkoff_portfolio_position: TinkoffPortfolioPosition) -> PortfolioPosition:
        average_price = None
        average_price_no_nkd = None

        if tinkoff_portfolio_position.average_position_price is not None:
            average_price = MoneyAmountMapper.map(tinkoff_portfolio_position.average_position_price)

        if tinkoff_portfolio_position.average_position_price_no_nkd is not None:
            average_price_no_nkd = MoneyAmountMapper.map(tinkoff_portfolio_position.average_position_price_no_nkd)

        return PortfolioPosition(figi=tinkoff_portfolio_position.figi,
                                 isin=tinkoff_portfolio_position.isin,
                                 name=tinkoff_portfolio_position.name,
                                 ticker=tinkoff_portfolio_position.ticker,
                                 balance=tinkoff_portfolio_position.balance,
                                 lots=tinkoff_portfolio_position.lots,
                                 average_price=average_price,
                                 average_price_no_nkd=average_price_no_nkd
                                 )
