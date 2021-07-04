from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class PayInOperationsSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        self.__write_pay_in(portfolio)

    def __write_pay_in(self, portfolio: Portfolio):
        dates = CellIterator('A1')
        values = CellIterator('B1')

        self.worksheet.write(dates.__str__(), 'Date', self.formats.headers['OPERATIONS_GROUP'])
        self.worksheet.write(values.__str__(), 'Value', self.formats.headers['OPERATIONS_GROUP'])

        for operation in portfolio.pay_in_operations():
            dates.next_row()
            values.next_row()

            self.worksheet.write(dates.__str__(), operation.date, self.formats.dates['FULL'])
            self.worksheet.write(values.__str__(), operation.payment, self.formats.currency[operation.currency])

        dates.next_row()
        dates.next_row()

        values.next_row()
        values.next_row()

        total_pay_in = portfolio.total_pay_in()

        self.worksheet.write(dates.__str__(), 'Total RUB', self.formats.styles['BOLD'])
        self.worksheet.write(values.__str__(), total_pay_in.value, self.formats.currency[total_pay_in.currency])
