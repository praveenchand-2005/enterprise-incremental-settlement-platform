from decimal import Decimal
from .domain import Trip

def merge_trip_states(old: Trip, new: Trip) -> Trip:
    result = Trip(trip_id=old.trip_id, base_fare=old.base_fare,
                  tips=list(old.tips), refunds=list(old.refunds),
                  disputes=list(old.disputes), adjustments=list(old.adjustments),
                  attributes=dict(old.attributes))
    if new.base_fare != Decimal("0"):
        result.base_fare = new.base_fare
    for field, incoming in [("tips", new.tips), ("refunds", new.refunds),
                            ("disputes", new.disputes), ("adjustments", new.adjustments)]:
        current = getattr(result, field)
        seen = {x.source_event_id for x in current}
        for item in incoming:
            if item.source_event_id not in seen:
                current.append(item)
                seen.add(item.source_event_id)
    result.attributes.update(new.attributes)
    return result
