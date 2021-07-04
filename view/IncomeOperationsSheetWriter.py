from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class IncomeOperationsSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        self.__write_coupons(portfolio)
        self.__write_dividends(portfolio)

    def __write_coupons(self, portfolio: Portfolio):
        dates = CellIterator('A1')
        values = CellIterator('B1')

        self.worksheet.merge_range(
            dates.row_index(), dates.col_index(),
            values.row_index(), values.col_index(),
            'Coupons',
            self.formats.headers['OPERATIONS_GROUP']
        )
        dates.next_row()
        values.next_row()

        self.worksheet.write(dates.__str__(), 'Date', self.formats.headers['OPERATIONS_GROUP'])
        self.worksheet.write(values.__str__(), 'Value', self.formats.headers['OPERATIONS_GROUP'])

        for operation in portfolio.coupons():
            dates.next_row()
            values.next_row()

            self.worksheet.write(dates.__str__(), operation.date, self.formats.dates['FULL'])
            self.worksheet.write(values.__str__(), operation.payment, self.formats.currency[operation.currency])

    def __write_dividends(self, portfolio: Portfolio):
        dates = CellIterator('D1')
        values = CellIterator('E1')

        self.worksheet.merge_range(
            dates.row_index(), dates.col_index(),
            values.row_index(), values.col_index(),
            'Dividends',
            self.formats.headers['OPERATIONS_GROUP']
        )
        dates.next_row()
        values.next_row()

        self.worksheet.write(dates.__str__(), 'Date', self.formats.headers['OPERATIONS_GROUP'])
        self.worksheet.write(values.__str__(), 'Value', self.formats.headers['OPERATIONS_GROUP'])

        for operation in portfolio.dividends():
            dates.next_row()
            values.next_row()

            self.worksheet.write(dates.__str__(), operation.date, self.formats.dates['FULL'])
            self.worksheet.write(values.__str__(), operation.payment, self.formats.currency[operation.currency])
