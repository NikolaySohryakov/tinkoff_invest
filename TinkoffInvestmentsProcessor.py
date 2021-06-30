from datetime import datetime
from tinvest import clients


class TinkoffInvestmentsProcessor:
    api_key: str
    start_date: datetime

    def __init__(self, api_key: str, start_date: datetime):
        self.api_key = api_key
        self.start_date = start_date

    def process(self):
        pass