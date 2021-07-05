from copy import copy

from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio, PortfolioPosition
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class PortfolioSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        header_cell = CellIterator('A5')
        first_position_cell = CellIterator('A6')

        self.__write_market_rates(portfolio)
        self.__write_headers(start_cell=header_cell)
        last_cell = self.__write_positions(start_cell=first_position_cell, portfolio=portfolio)

        last_cell.next_row()
        last_cell.next_row()
        last_cell.col = 'A'

        self.__write_summary(start_cell = last_cell, portfolio=portfolio)

    def __write_market_rates(self, portfolio):
        self.worksheet.merge_range(0, 0,
                                   0, 1,
                                   'Market Rates',
                                   self.formats.headers['OPERATIONS_GROUP'])

        currency_cell = CellIterator('A2')
        rate_cell = CellIterator('B2')

        for currency, rate in portfolio.market_rates.items():
            if currency == 'RUB':
                continue

            self.worksheet.write(currency_cell.__str__(), currency)
            self.worksheet.write(rate_cell.__str__(), rate)

    def __write_headers(self, start_cell):
        headers = ['Name', 'Ticker', 'Balance', 'Currency', 'Average Price', 'Buy', 'Expected Yield', 'Market Price',
                   '% change', 'Market Value', 'Market Value RUB']

        for header in headers:
            self.worksheet.write(start_cell.__str__(), header, self.formats.headers['PORTFOLIO'])
            start_cell.next_col()

    def __write_positions(self, start_cell, portfolio: Portfolio):
        cell = copy(start_cell)

        for position in portfolio.positions:
            average_buy = position.average_buy()
            market_price = position.market_price()
            market_value = position.market_value()
            market_value_rub = portfolio.convert(position.market_value(), 'RUB')

            values = [
                (position.name, None),
                (position.ticker, None),
                (position.balance, None),
                (position.average_price.currency, None),
                (position.average_price.value, self.formats.currency[position.average_price.currency]),
                (average_buy.value, self.formats.currency[average_buy.currency]),
                (position.expected_yield.value, self.formats.currency[position.average_price.currency]),
                (market_price.value, self.formats.currency[market_price.currency]),
                (position.change_percent(), None),
                (market_value.value, self.formats.currency[market_value.currency]),
                (market_value_rub.value, self.formats.currency[market_value_rub.currency]),
            ]

            for col_num, value in enumerate(values):
                self.worksheet.write(cell.row_index(), cell.col_index() + col_num, value[0], value[1])

            cell.next_row()

        return cell

    def __write_summary(self, start_cell, portfolio: Portfolio):
        cell = copy(start_cell)

        self.worksheet.write(cell.__str__(), 'Pay In - Pay Out', self.formats.styles['BOLD_ALIGNMENT_RIGHT'])
        cell.next_col()
        self.worksheet.write(cell.__str__(), portfolio.adjusted_pay_in().value)
