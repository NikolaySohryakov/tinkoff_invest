from pycbrf import ExchangeRates


class ExchangeRatesProvider:
    @staticmethod
    def rates(on_date):
        rates = ExchangeRates(on_date=on_date, locale_en=True)

        return {
            'USD': rates['USD'].value,
            'EUR': rates['EUR'].value,
        }
