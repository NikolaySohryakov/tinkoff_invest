from copy import copy

from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class CommissionsSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        self.__write_broker_commissions(portfolio)
        self.__write_exchange_commissions(portfolio)
        self.__write_service_commissions(portfolio)
        self.__write_margin_commissions(portfolio)
        self.__write_other_commissions(portfolio)

    def __write_broker_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('A1')
        self.__write_operations(start_cell=start_cell,
                                name='Broker Commissions',
                                operations=portfolio.broker_commissions())

    def __write_exchange_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('D1')
        self.__write_operations(start_cell=start_cell,
                                name='Exchange Commissions',
                                operations=portfolio.exchange_commissions())

    def __write_service_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('G1')
        self.__write_operations(start_cell=start_cell,
                                name='Service Commissions',
                                operations=portfolio.service_commissions())

    def __write_margin_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('J1')
        self.__write_operations(start_cell=start_cell,
                                name='Margin Commissions',
                                operations=portfolio.margin_commissions())

    def __write_other_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('M1')
        self.__write_operations(start_cell=start_cell,
                                name='Other Commissions',
                                operations=portfolio.other_commissions())

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
