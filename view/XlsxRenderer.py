from dataclasses import dataclass
from decimal import Decimal

import xlsxwriter
from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from portfolio import PortfolioPosition
from portfolio import MoneyAmount
from view.PortfolioSheetWriter import PortfolioSheetWriter
from view.WorkbookFormats import WorkbookFormats


class XlsxRenderer:
    def __init__(self, output_file_path):
        self.workbook = xlsxwriter.Workbook(output_file_path)
        self.__prepare_formats()

    def render_portfolio(self, portfolio: Portfolio):
        portfolio_worksheet = self.workbook.add_worksheet(name='Portfolio')

        self.__write_portfolio_sheet(worksheet=portfolio_worksheet, portfolio=portfolio)

        self.workbook.close()

    def __prepare_formats(self):
        currency = {
            'USD': self.workbook.add_format({
                'num_format': '$ #,##0.00',
                'align': 'right'
            }),
            'RUB': self.workbook.add_format({
                'num_format': 'RUR #,##0.00',
                'align': 'right'
            })
        }

        headers = {
            'PORTFOLIO': self.workbook.add_format({
                'bold': True,
                'bg_color': '#CCCCCC',
                'align': 'center'
            })
        }

        self.formats = WorkbookFormats(currency=currency, headers=headers)

    def __write_portfolio_sheet(self, worksheet: Worksheet, portfolio):
        sheet_writer = PortfolioSheetWriter(worksheet=worksheet, formats=self.formats)
        sheet_writer.write(portfolio)


portfolio = Portfolio()
portfolio.positions = [
    PortfolioPosition(figi='figi1',
                      isin='isin1',
                      name='name1',
                      ticker='ticker1',
                      balance=Decimal('10'),
                      lots=10,
                      average_price=MoneyAmount(value=Decimal('100.34'),
                                                currency='RUB'),
                      average_price_no_nkd=MoneyAmount(value=Decimal('100.02'),
                                                       currency='RUB')),
    PortfolioPosition(figi='figi1',
                      isin='isin1',
                      name='name1',
                      ticker='ticker1',
                      balance=Decimal('15'),
                      lots=10,
                      average_price=MoneyAmount(value=Decimal('100.23'),
                                                currency='USD'),
                      average_price_no_nkd=MoneyAmount(value=Decimal('100.2'),
                                                       currency='USD'))

]
renderer = XlsxRenderer('/Users/nsohryakov/workspace/tinkoff_parser/view/output.xlsx')
renderer.render_portfolio(portfolio)
