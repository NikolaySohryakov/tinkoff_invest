from dataclasses import dataclass
from decimal import Decimal
from functools import reduce
from typing import Optional


@dataclass
class PortfolioPosition:
    figi: str
    name: str
    ticker: Optional[str]
    balance: Decimal

    def __radd__(self, other):
        return other + self.balance


class Portfolio:
    positions: [PortfolioPosition]

    def __init__(self, positions):
        self.positions = positions

    def average(self) -> Decimal:
        return sum(self.positions) / len(self.positions)
