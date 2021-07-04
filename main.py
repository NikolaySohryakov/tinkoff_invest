from portfolio import TinkoffPortfolioLoader
from datetime import datetime
from tinvest import SyncClient as TInvestClient
import configparser

from view.XlsxRenderer import XlsxRenderer

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.txt')

    start_date = datetime.strptime(config['DEFAULT']['StartDate'], "%d.%m.%Y")
    production_token = config['API']['ProductionToken']
    sandbox_token = config['API']['SandboxToken']
    use_sandbox = config['API'].getboolean('UseSandbox', fallback=True)

    token = sandbox_token if use_sandbox else production_token

    client = TInvestClient(token=token, use_sandbox=use_sandbox)

    portfolio_loader = TinkoffPortfolioLoader(client=client, start_date=start_date)
    portfolio = portfolio_loader.load()

    xlsx_writer = XlsxRenderer('/Users/nsohryakov/workspace/tinkoff_parser/view/output.xlsx')
    xlsx_writer.render_portfolio(portfolio)
