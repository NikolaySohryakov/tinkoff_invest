from copy import copy

from xlsxwriter.worksheet import Worksheet

from portfolio import Portfolio, PortfolioPosition
from view.CellIterator import CellIterator
from view.WorkbookFormats import WorkbookFormats


class OperationsSheetWriter:
    def __init__(self, worksheet: Worksheet, formats: WorkbookFormats):
        self.worksheet = worksheet
        self.formats = formats

    def write(self, portfolio: Portfolio):
        self.worksheet.write('A1', 'hello world')
