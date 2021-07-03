from portfolio import Operation


class OperationMapper:
    @staticmethod
    def map(tinkoff_operation) -> Operation:
        return Operation(id=tinkoff_operation.id,
                         figi=tinkoff_operation.figi,
                         date=tinkoff_operation.date,
                         currency=tinkoff_operation.currency.value,
                         payment=tinkoff_operation.payment
                         )
