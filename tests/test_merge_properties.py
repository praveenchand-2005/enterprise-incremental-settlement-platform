from decimal import Decimal
from platform_core.domain import Trip, Adjustment
from platform_core.merge_contract import merge_trip_states

def trip(events):
    t = Trip("t1", base_fare=Decimal("100"))
    fields = {"tip":"tips", "refund":"refunds", "dispute":"disputes", "adjustment":"adjustments"}
    for kind, amount, eid in events:
        getattr(t, fields[kind]).append(Adjustment(kind, Decimal(str(amount)), eid))
    return t

def sig(t):
    return (t.base_fare,
            sorted((x.source_event_id, str(x.amount)) for x in t.tips),
            sorted((x.source_event_id, str(x.amount)) for x in t.refunds),
            sorted((x.source_event_id, str(x.amount)) for x in t.disputes),
            sorted((x.source_event_id, str(x.amount)) for x in t.adjustments))

def test_merge_identity():
    a = trip([("tip", 10, "a")])
    assert sig(merge_trip_states(a, Trip("t1"))) == sig(a)

def test_merge_idempotence():
    a = trip([("tip", 10, "a"), ("refund", 5, "b")])
    assert sig(merge_trip_states(a, a)) == sig(a)

def test_merge_associativity():
    a, b, c = trip([("tip",10,"a")]), trip([("refund",5,"b")]), trip([("dispute",2,"c")])
    assert sig(merge_trip_states(merge_trip_states(a,b),c)) == sig(merge_trip_states(a,merge_trip_states(b,c)))
