from unittest.mock import Mock


def __operation_type(type_) -> Mock:
    operation_type_ = Mock()
    operation_type_.value = type
    return operation_type_


operations = [
            Mock(
                operation_type=__operation_type('Buy')
            ),
            Mock(
                operation_type=__operation_type('BuyCard')
            ),
            Mock(
                operation_type=__operation_type('Sell')
            ),
            Mock(
                operation_type=__operation_type('BrokerCommission')
            ),
            Mock(
                operation_type=__operation_type('ExchangeCommission')
            ),
            Mock(
                operation_type=__operation_type('ServiceCommission')
            ),
            Mock(
                operation_type=__operation_type('MarginCommission')
            ),
            Mock(
                operation_type=__operation_type('OtherCommission')
            ),
            Mock(
                operation_type=__operation_type('PayIn')
            ),
            Mock(
                operation_type=__operation_type('PayOut')
            ),
            Mock(
                operation_type=__operation_type('Tax')
            ),
            Mock(
                operation_type=__operation_type('TaxLucre')
            ),
            Mock(
                operation_type=__operation_type('TaxDividend')
            ),
            Mock(
                operation_type=__operation_type('TaxCoupon')
            ),
            Mock(
                operation_type=__operation_type('TaxBack')
            ),
            Mock(
                operation_type=__operation_type('Repayment')
            ),
            Mock(
                operation_type=__operation_type('PartRepayment')
            ),
            Mock(
                operation_type=__operation_type('Coupon')
            ),
            Mock(
                operation_type=__operation_type('Dividend')
            ),
            Mock(
                operation_type=__operation_type('SecurityIn')
            ),
            Mock(
                operation_type=__operation_type('SecurityOut')
            )
        ]
