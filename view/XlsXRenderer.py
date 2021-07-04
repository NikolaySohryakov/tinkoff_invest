from copy import copy
from decimal import Decimal
import re

import xlsxwriter
from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from portfolio import PortfolioPosition
from portfolio import MoneyAmount


cell_index_parts = re.compile(r'(\$?)([A-Z]{1,3})(\$?)(\d+)')


class CellIterator:
    def __init__(self, *args, **kwargs):
        try:
            # First arg is an int, default to row/col notation.
            if len(kwargs) == 2:
                self.row = kwargs['row']
                self.col = kwargs['col']
            else:
                raise ValueError
        except ValueError:
            match = cell_index_parts.match(args[0])
            col_str = match.group(2)
            row = int(match.group(4))

            self.col = col_str
            self.row = row

    def next_row(self):
        self.row += 1

    def next_col(self):
        if self.col[-1:].upper() == 'Z':
            self.col = 'A' + self.col[:-1] + 'A'
        else:
            next_char = chr(ord(self.col[-1:]) + 1)

            self.col = self.col[:-1] + next_char

    def col_index(self) -> int:
        """Zero-based index or a column."""
        result = 0

        for index, char in enumerate(self.col):
            result += ord(char.upper()) - ord('A') + (ord('Z') - ord('A') + 1) * index

        return result

    def row_index(self) -> int:
        """Zero-based index of a row."""
        return self.row - 1

    def __str__(self):
        return self.col.upper() + str(self.row)


class XlsxRenderer:
    def __init__(self, output_file_path):
        self.workbook = xlsxwriter.Workbook(output_file_path)
        self.__prepare_formats()

    def render_portfolio(self, portfolio: Portfolio):
        portfolio_worksheet = self.workbook.add_worksheet(name='Portfolio')

        self.__write_portfolio_sheet(worksheet=portfolio_worksheet, portfolio=portfolio)

        self.workbook.close()

    def __prepare_formats(self):
        self.currency_format = {
            'USD': self.workbook.add_format({
                'num_format': '$ #,##0.00',
                'align': 'right'
            }),
            'RUB': self.workbook.add_format({
                'num_format': 'RUR #,##0.00',
                'align': 'right'
            })
        }

    def __write_portfolio_sheet(self, worksheet: Worksheet, portfolio):
        header_cell = CellIterator('A1')
        first_position_cell = CellIterator('A2')

        self.__write_headers(start_cell=header_cell, worksheet=worksheet)
        self.__write_positions(start_cell=first_position_cell, worksheet=worksheet, positions=portfolio.positions)

    def __write_headers(self, start_cell, worksheet: Worksheet):
        cell_format = self.workbook.add_format({
            'bold': True,
            'bg_color': '#CCCCCC',
            'align': 'center'
        })

        headers = ['Name', 'Ticker', 'Balance', 'Currency', 'Average Price']

        for header in headers:
            worksheet.write(start_cell.__str__(), header, cell_format)
            start_cell.next_col()

    def __write_positions(self, start_cell, worksheet: Worksheet, positions: [PortfolioPosition]):
        cell = copy(start_cell)

        for position in positions:
            values = [
                (position.name, None),
                (position.ticker, None),
                (position.balance, None),
                (position.average_price.currency, None),
                (position.average_price.value, self.currency_format[position.average_price.currency])
            ]

            for col_num, value in enumerate(values):
                worksheet.write(cell.row_index(), cell.col_index() + col_num, value[0], value[1])

            cell.next_row()


# portfolio.positions = [
#     PortfolioPosition(figi='figi1',
#                       isin='isin1',
#                       name='name1',
#                       ticker='ticker1',
#                       balance=Decimal('10'),
#                       lots=10,
#                       average_price=MoneyAmount(value=Decimal('100.34'),
#                                                 currency='RUB'),
#                       average_price_no_nkd=MoneyAmount(value=Decimal('100.02'),
#                                                        currency='RUB')),
#     PortfolioPosition(figi='figi1',
#                       isin='isin1',
#                       name='name1',
#                       ticker='ticker1',
#                       balance=Decimal('15'),
#                       lots=10,
#                       average_price=MoneyAmount(value=Decimal('100.23'),
#                                                 currency='USD'),
#                       average_price_no_nkd=MoneyAmount(value=Decimal('100.2'),
#                                                        currency='USD'))
#
# ]
# portfolio = Portfolio()
# renderer = XlsxRenderer('/Users/nsohryakov/workspace/tinkoff_parser/view/output.xlsx')
# renderer.render_portfolio(portfolio)
