from portfolio import MoneyAmount


class MoneyAmountMapper:
    @staticmethod
    def map(tinkoff_money_amount) -> MoneyAmount:
        return MoneyAmount(value=tinkoff_money_amount.value,
                           currency=tinkoff_money_amount.currency.value)
