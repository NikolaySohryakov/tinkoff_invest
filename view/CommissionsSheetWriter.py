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
        cell1 = self.__write_broker_commissions(portfolio)
        cell2 = self.__write_exchange_commissions(portfolio)
        cell3 = self.__write_service_commissions(portfolio)
        cell4 = self.__write_margin_commissions(portfolio)
        cell5 = self.__write_other_commissions(portfolio)

        indices = [cell1.row_index(),
                   cell2.row_index(),
                   cell3.row_index(),
                   cell4.row_index(),
                   cell5.row_index()]

        next_cell_index = max(indices) + 3
        self.__write_summary(CellIterator(col='A', row=next_cell_index), portfolio)

    def __write_broker_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('A1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Broker Commissions',
                                       operations=portfolio.broker_commissions())

    def __write_exchange_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('D1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Exchange Commissions',
                                       operations=portfolio.exchange_commissions())

    def __write_service_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('G1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Service Commissions',
                                       operations=portfolio.service_commissions())

    def __write_margin_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('J1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Margin Commissions',
                                       operations=portfolio.margin_commissions())

    def __write_other_commissions(self, portfolio: Portfolio):
        start_cell = CellIterator('M1')
        return self.__write_operations(start_cell=start_cell,
                                       name='Other Commissions',
                                       operations=portfolio.other_commissions())

    def __write_summary(self, start_cell, portfolio: Portfolio):
        cell = copy(start_cell)

        total_broker = portfolio.total_broker_commissions()
        total_exchange = portfolio.total_exchange_commissions()
        total_service = portfolio.total_service_commissions()
        total_margin = portfolio.total_margin_commissions()
        total_other = portfolio.total_other_commissions()
        total_all = portfolio.total_all_commissions()

        self.__write_summary_row(cell, 'Broker Total', total_broker)
        cell.next_row()
        self.__write_summary_row(cell, 'Exchange Total', total_exchange)
        cell.next_row()
        self.__write_summary_row(cell, 'Service Total', total_service)
        cell.next_row()
        self.__write_summary_row(cell, 'Margin Total', total_margin)
        cell.next_row()
        self.__write_summary_row(cell, 'Other Total', total_other)
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
