from copy import copy

from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class TaxSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        self.__write_tax_dividend(portfolio)
        self.__write_tax_coupon(portfolio)
        self.__write_tax_common(portfolio)
        self.__write_tax_lucre(portfolio)
        self.__write_tax_back(portfolio)

    def __write_tax_dividend(self, portfolio: Portfolio):
        start_cell = CellIterator('A1')
        self.__write_operations(start_cell=start_cell,
                                name='Dividend',
                                operations=portfolio.tax_dividend())

    def __write_tax_coupon(self, portfolio: Portfolio):
        start_cell = CellIterator('D1')
        self.__write_operations(start_cell=start_cell,
                                name='Coupon',
                                operations=portfolio.tax_coupon())

    def __write_tax_common(self, portfolio: Portfolio):
        start_cell = CellIterator('G1')
        self.__write_operations(start_cell=start_cell,
                                name='Other',
                                operations=portfolio.tax_common())

    def __write_tax_lucre(self, portfolio: Portfolio):
        start_cell = CellIterator('J1')
        self.__write_operations(start_cell=start_cell,
                                name='Lucre',
                                operations=portfolio.tax_lucre())

    def __write_tax_back(self, portfolio: Portfolio):
        start_cell = CellIterator('M1')
        self.__write_operations(start_cell=start_cell,
                                name='Tax Back',
                                operations=portfolio.tax_back())

    def __write_operations(self, start_cell, name, operations):
        dates = copy(start_cell)
        values = copy(start_cell)
        values.next_col()

        self.worksheet.merge_range(
            dates.row_index(), dates.col_index(),
            values.row_index(), values.col_index(),
            name,
            self.formats.headers['OPERATIONS_GROUP']
        )
        dates.next_row()
        values.next_row()

        self.worksheet.write(dates.__str__(), 'Date', self.formats.headers['OPERATIONS_GROUP'])
        self.worksheet.write(values.__str__(), 'Value', self.formats.headers['OPERATIONS_GROUP'])

        for operation in operations:
            dates.next_row()
            values.next_row()

            self.worksheet.write(dates.__str__(), operation.date, self.formats.dates['FULL'])
            self.worksheet.write(values.__str__(), operation.payment, self.formats.currency[operation.currency])
