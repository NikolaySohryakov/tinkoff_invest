from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

import xlsxwriter

from portfolio import Portfolio, Operation
from portfolio import PortfolioPosition
from portfolio import MoneyAmount
from view.BuyOperationsSheetWriter import BuyOperationsSheetWriter
from view.CommissionsSheetWriter import CommissionsSheetWriter
from view.IncomeOperationsSheetWriter import IncomeOperationsSheetWriter
from view.PayInOperationsSheetWriter import PayInOperationsSheetWriter
from view.PayOutOperationsSheetWriter import PayOutOperationsSheetWriter
from view.PortfolioSheetWriter import PortfolioSheetWriter
from view.SellOperationsSheetWriter import SellOperationsSheetWriter
from view.WorkbookFormats import WorkbookFormats


class XlsxRenderer:
    def __init__(self, output_file_path):
        self.workbook = xlsxwriter.Workbook(output_file_path)
        self.workbook.remove_timezone = True
        self.__prepare_formats()

    def render_portfolio(self, portfolio: Portfolio):
        portfolio_worksheet = self.workbook.add_worksheet(name='Portfolio')
        pay_in_worksheet = self.workbook.add_worksheet(name='Pay In')
        pay_out_worksheet = self.workbook.add_worksheet(name='Pay Out')
        buy_worksheet = self.workbook.add_worksheet(name='Buy')
        sell_worksheet = self.workbook.add_worksheet(name='Sell')
        income_worksheet = self.workbook.add_worksheet(name='Income')
        commissions_worksheet = self.workbook.add_worksheet(name='Commissions')

        writers = [
            PortfolioSheetWriter(worksheet=portfolio_worksheet, formats=self.formats),
            PayInOperationsSheetWriter(worksheet=pay_in_worksheet, formats=self.formats),
            PayOutOperationsSheetWriter(worksheet=pay_out_worksheet, formats=self.formats),
            BuyOperationsSheetWriter(worksheet=buy_worksheet, formats=self.formats),
            SellOperationsSheetWriter(worksheet=sell_worksheet, formats=self.formats),
            IncomeOperationsSheetWriter(worksheet=income_worksheet, formats=self.formats),
            CommissionsSheetWriter(worksheet=commissions_worksheet, formats=self.formats)
        ]

        for writer in writers:
            writer.write(portfolio)

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
            }),
            'OPERATIONS_GROUP': self.workbook.add_format({
                'bold': True,
                'align': 'center'
            })
        }

        dates = {
            'FULL': self.workbook.add_format({
                'num_format': 'mmm d yyyy, HH:mm'
            })
        }

        self.formats = WorkbookFormats(currency=currency,
                                       headers=headers,
                                       dates=dates)


# portfolio = Portfolio()
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
# portfolio.operations = [
#     Operation(id='id',
#               figi='figi',
#               date=datetime.now(),
#               currency='USD',
#               payment=Decimal('100.3')),
#     Operation(id='id1',
#               figi='figi1',
#               date=datetime.now(),
#               currency='RUB',
#               payment=Decimal('23.5'))
# ]
# renderer = XlsxRenderer('/Users/nsohryakov/workspace/tinkoff_parser/view/output.xlsx')
# renderer.render_portfolio(portfolio)
