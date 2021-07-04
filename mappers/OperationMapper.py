from portfolio import Operation
from tinvest import Operation as TinkoffOperation


class OperationMapper:
    @staticmethod
    def map(tinkoff_operation: TinkoffOperation) -> Operation:
        return Operation(id=tinkoff_operation.id,
                         figi=tinkoff_operation.figi,
                         date=tinkoff_operation.date,
                         currency=tinkoff_operation.currency.value,
                         payment=tinkoff_operation.payment,
                         commission=tinkoff_operation.commission,
                         operation_type=tinkoff_operation.operation_type.value,
                         price=tinkoff_operation.price,
                         quantity=tinkoff_operation.quantity,
                         status=tinkoff_operation.status.value
                         )
