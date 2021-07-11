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

        self.worksheet.set_column('A:A', 35)
        self.worksheet.set_column('B:B', 15)
        self.worksheet.set_column('C:C', 8)
        self.worksheet.set_column('D:D', 9)
        self.worksheet.set_column('E:E', 14)
        self.worksheet.set_column('F:F', 14)
        self.worksheet.set_column('G:G', 14)
        self.worksheet.set_column('H:H', 18)
        self.worksheet.set_column('I:I', 10)
        self.worksheet.set_column('J:J', 14)
        self.worksheet.set_column('K:K', 18)

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

            self.worksheet.write_string(currency_cell.__str__(), currency)
            self.worksheet.write_number(rate_cell.__str__(), rate)

    def __write_headers(self, start_cell):
        headers = ['Name', 'Ticker', 'Balance', 'Currency', 'Average Price', 'Buy', 'Expected Yield', 'Market Price',
                   '% change', 'Market Value', 'Market Value RUB']

        self.worksheet.write_row(start_cell.__str__(), headers, self.formats.headers['PORTFOLIO'])

    def __write_positions(self, start_cell, portfolio: Portfolio):
        cell = copy(start_cell)

        for position in portfolio.positions:
            average_buy = position.average_buy()
            market_price = position.market_price()
            market_value = position.market_value()
            market_value_rub = portfolio.convert(position.market_value(), 'RUB')
            change_percent = position.change_percent()

            values = [
                (position.name, None),
                (position.ticker, None),
                (position.balance, None),
                (position.average_price.currency, self.formats.styles["ALIGNMENT_CENTER"]),
                (position.average_price.value, self.formats.currency[position.average_price.currency]),
                (average_buy.value, self.formats.currency[average_buy.currency]),
                (position.expected_yield.value, self.formats.currency[position.average_price.currency]),
                (market_price.value, self.formats.currency[market_price.currency]),
                (change_percent, self.__percent_change_format(change_percent)),
                (market_value.value, self.formats.currency[market_value.currency]),
                (market_value_rub.value, self.formats.currency[market_value_rub.currency]),
            ]

            for col_num, value in enumerate(values):
                self.worksheet.write(cell.row_index(), cell.col_index() + col_num, value[0], value[1])

            cell.next_row()

        return cell

    def __percent_change_format(self, change):
        change_percent_format = None
        if change > 0:
            change_percent_format = self.formats.styles['GREEN']
        elif change < 0:
            change_percent_format = self.formats.styles['RED']

        return change_percent_format

    def __write_summary(self, start_cell, portfolio: Portfolio):
        cell = copy(start_cell)

        percent_change = portfolio.percent_change()

        rows = [
            ('Pay In - Pay Out', portfolio.adjusted_pay_in().value, self.formats.currency['RUB']),
            ('Market Value', portfolio.market_value().value, self.formats.currency['RUB']),
            ('Average % change', portfolio.percent_change(), self.__percent_change_format(percent_change))
        ]

        for title, value, cell_format in rows:
            self.__write_summary_row(cell, title, value, cell_format)
            cell.next_row()

    def __write_summary_row(self, start_cell, title, value, cell_format=None):
        cell = copy(start_cell)

        self.worksheet.write(cell.__str__(), title, self.formats.styles['BOLD_ALIGNMENT_RIGHT'])
        cell.next_col()
        self.worksheet.write(cell.__str__(), value, cell_format)
