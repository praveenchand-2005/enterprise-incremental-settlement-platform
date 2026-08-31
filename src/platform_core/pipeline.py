from decimal import Decimal
from .domain import Trip, Adjustment
from .merge_contract import merge_trip_states
from .rules import settlement_total

class TripCollectionPipeline:
    def __init__(self):
        self.state = {}
        self.seen_events = set()

    def process(self, events):
        affected = {}
        for e in events:
            eid = e["event_id"]
            if eid in self.seen_events:
                continue
            self.seen_events.add(eid)
            tid = e["entity_id"]
            partial = Trip(tid)
            amount = Decimal(str(e["amount"]))
            if e["event_type"] == "trip_completed":
                partial.base_fare = amount
            elif e["event_type"] == "tip":
                partial.tips.append(Adjustment("tip", amount, eid))
            elif e["event_type"] == "refund":
                partial.refunds.append(Adjustment("refund", abs(amount), eid))
            elif e["event_type"] == "dispute":
                partial.disputes.append(Adjustment("dispute", abs(amount), eid))
            else:
                partial.adjustments.append(Adjustment(e["event_type"], amount, eid))
            self.state[tid] = merge_trip_states(self.state.get(tid, Trip(tid)), partial)
            affected[tid] = settlement_total(self.state[tid])
        return affected, {k: settlement_total(self.state[k]) for k in affected}
