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
        cell1 = self.__write_tax_dividend(portfolio)
        cell2 = self.__write_tax_coupon(portfolio)
        cell3 = self.__write_tax_common(portfolio)
        cell4 = self.__write_tax_lucre(portfolio)
        cell5 = self.__write_tax_back(portfolio)

        indices = [cell1.row_index(),
                   cell2.row_index(),
                   cell3.row_index(),
                   cell4.row_index(),
                   cell5.row_index()]

        next_cell_index = max(indices) + 3
        self.__write_summary(CellIterator(col='A', row=next_cell_index), portfolio)

    def __write_tax_dividend(self, portfolio: Portfolio):
        start_cell = CellIterator('A1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Dividend',
                                       operations=portfolio.tax_dividend())

    def __write_tax_coupon(self, portfolio: Portfolio):
        start_cell = CellIterator('D1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Coupon',
                                       operations=portfolio.tax_coupon())

    def __write_tax_common(self, portfolio: Portfolio):
        start_cell = CellIterator('G1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Other',
                                       operations=portfolio.tax_common())

    def __write_tax_lucre(self, portfolio: Portfolio):
        start_cell = CellIterator('J1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Lucre',
                                       operations=portfolio.tax_lucre())

    def __write_tax_back(self, portfolio: Portfolio):
        start_cell = CellIterator('M1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Tax Back',
                                       operations=portfolio.tax_back())

    def __write_summary(self, start_cell, portfolio: Portfolio):
        cell = copy(start_cell)

        total_common = portfolio.tax_common_total()
        total_dividend = portfolio.tax_dividend_total()
        total_coupon = portfolio.tax_coupon_total()
        total_lucre = portfolio.tax_lucre_total()
        total_back = portfolio.tax_back_total()
        total_all = portfolio.tax_total()

        self.__write_summary_row(cell, 'Common Total', total_common)
        cell.next_row()
        self.__write_summary_row(cell, 'Dividend Total', total_dividend)
        cell.next_row()
        self.__write_summary_row(cell, 'Coupon Total', total_coupon)
        cell.next_row()
        self.__write_summary_row(cell, 'Lucre Total', total_lucre)
        cell.next_row()
        self.__write_summary_row(cell, 'Tax Back Total', total_back)
        cell.next_row()
        cell.next_row()
        self.__write_summary_row(cell, 'Total', total_all)

    def __write_summary_row(self, cell, title, amount):
        title_cell = copy(cell)
        value_cell = copy(cell)

        value_cell.next_col()

        self.worksheet.write(title_cell.__str__(), title, self.formats.styles['BOLD_ALIGNMENT_RIGHT'])
        self.worksheet.write(value_cell.__str__(), amount.value, self.formats.currency[amount.currency])

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

        return dates
