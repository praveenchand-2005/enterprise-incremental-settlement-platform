from dataclasses import dataclass, field
from decimal import Decimal

@dataclass
class Adjustment:
    kind: str
    amount: Decimal
    source_event_id: str

@dataclass
class Trip:
    trip_id: str
    base_fare: Decimal = Decimal("0")
    tips: list[Adjustment] = field(default_factory=list)
    refunds: list[Adjustment] = field(default_factory=list)
    disputes: list[Adjustment] = field(default_factory=list)
    adjustments: list[Adjustment] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)

    @property
    def refund_total(self):
        return sum((x.amount for x in self.refunds), Decimal("0"))

    @property
    def tip_total(self):
        return sum((x.amount for x in self.tips), Decimal("0"))
