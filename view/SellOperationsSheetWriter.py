from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class SellOperationsSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        self.__write_sell(portfolio)

        self.worksheet.set_column('A:B', 16)

    def __write_sell(self, portfolio: Portfolio):
        dates = CellIterator('A1')
        values = CellIterator('B1')

        self.worksheet.write(dates.__str__(), 'Date', self.formats.headers['OPERATIONS_GROUP'])
        self.worksheet.write(values.__str__(), 'Value', self.formats.headers['OPERATIONS_GROUP'])

        for operation in portfolio.sell_operations():
            dates.next_row()
            values.next_row()

            self.worksheet.write_datetime(dates.__str__(), operation.date, self.formats.dates['FULL'])
            self.worksheet.write(values.__str__(), operation.payment, self.formats.currency[operation.currency])

        dates.next_row()
        dates.next_row()

        values.next_row()
        values.next_row()

        total_pay_in = portfolio.sell_total()

        self.worksheet.write(dates.__str__(), 'Total RUB', self.formats.styles['BOLD'])
        self.worksheet.write(values.__str__(), total_pay_in.value, self.formats.currency[total_pay_in.currency])
