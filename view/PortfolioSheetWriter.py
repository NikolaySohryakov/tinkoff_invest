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
        header_cell = CellIterator('A1')
        first_position_cell = CellIterator('A2')

        self.__write_headers(start_cell=header_cell)
        self.__write_positions(start_cell=first_position_cell, positions=portfolio.positions)

    def __write_headers(self, start_cell):
        headers = ['Name', 'Ticker', 'Balance', 'Currency', 'Average Price']

        for header in headers:
            self.worksheet.write(start_cell.__str__(), header, self.formats.headers['PORTFOLIO'])
            start_cell.next_col()

    def __write_positions(self, start_cell, positions: [PortfolioPosition]):
        cell = copy(start_cell)

        for position in positions:
            values = [
                (position.name, None),
                (position.ticker, None),
                (position.balance, None),
                (position.average_price.currency, None),
                (position.average_price.value, self.formats.currency[position.average_price.currency])
            ]

            for col_num, value in enumerate(values):
                self.worksheet.write(cell.row_index(), cell.col_index() + col_num, value[0], value[1])

            cell.next_row()
