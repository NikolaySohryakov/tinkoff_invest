from TinkoffInvestmentsProcessor import TinkoffInvestmentsProcessor
from datetime import datetime
import configparser


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.txt')

    api_key = config['DEFAULT']['APIKey']
    start_date = datetime.strptime(config['DEFAULT']['StartDate'], "%d.%m.%Y")

    processor = TinkoffInvestmentsProcessor(api_key=api_key, start_date=start_date)
    processor.process()
