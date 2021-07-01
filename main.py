from Portfolio.TinkoffPortfolioLoader import TinkoffPortfolioLoader
from Portfolio.TinkoffPortfolioLoader import TinkoffConfig
from datetime import datetime
from tinvest import SyncClient as TInvestClient
import configparser


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.txt')

    start_at = datetime.strptime(config['DEFAULT']['StartDate'], "%d.%m.%Y")
    production_token = config['API']['ProductionToken']
    sandbox_token = config['API']['SandboxToken']
    use_sandbox = config['API'].getboolean('UseSandbox', fallback=True)

    config = TinkoffConfig(production_token=production_token,
                           sandbox_token=sandbox_token,
                           use_sandbox=use_sandbox)

    client = TInvestClient(token=config.token(), use_sandbox=config.use_sandbox)

    processor = TinkoffPortfolioLoader(client=client, start_at=start_at)
    processor.load()
