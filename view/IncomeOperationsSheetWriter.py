from copy import copy

from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class IncomeOperationsSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        coupons_last_cell = self.__write_coupons(portfolio)
        dividends_last_cell = self.__write_dividends(portfolio)

        last_row = coupons_last_cell.row if coupons_last_cell.row > dividends_last_cell.row else dividends_last_cell.row
        cell = CellIterator(row=last_row+2, col='A')
        self.__write_summary(cell=cell, portfolio=portfolio)

        self.worksheet.set_column('A:B', 18)
        self.worksheet.set_column('D:E', 18)

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

            self.worksheet.write_datetime(dates.__str__(), operation.date, self.formats.dates['FULL'])
            self.worksheet.write(values.__str__(), operation.payment, self.formats.currency[operation.currency])

        return dates

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

            self.worksheet.write_datetime(dates.__str__(), operation.date, self.formats.dates['FULL'])
            self.worksheet.write(values.__str__(), operation.payment, self.formats.currency[operation.currency])

        return dates

    def __write_summary(self, cell, portfolio):
        text_cell = copy(cell)
        value_cell = copy(cell)

        value_cell.next_col()

        total_coupons = portfolio.coupons_total()
        total_dividends = portfolio.dividends_total()
        total_income = portfolio.income_total()

        self.worksheet.write(text_cell.__str__(), 'Total Coupons', self.formats.styles['BOLD'])
        self.worksheet.write(value_cell.__str__(), total_coupons.value, self.formats.currency[total_coupons.currency])

        text_cell.next_row()
        value_cell.next_row()

        self.worksheet.write(text_cell.__str__(), 'Total Dividends', self.formats.styles['BOLD'])
        self.worksheet.write(value_cell.__str__(), total_dividends.value, self.formats.currency[total_dividends.currency])

        text_cell.next_row()
        value_cell.next_row()
        text_cell.next_row()
        value_cell.next_row()

        self.worksheet.write(text_cell.__str__(), 'Total', self.formats.styles['BOLD'])
        self.worksheet.write(value_cell.__str__(), total_income.value, self.formats.currency[total_income.currency])
