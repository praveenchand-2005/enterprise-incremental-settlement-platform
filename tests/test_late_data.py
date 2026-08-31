from decimal import Decimal
from platform_core.pipeline import TripCollectionPipeline

def test_old_trip_can_receive_new_refund():
    p = TripCollectionPipeline()
    p.process([{"event_id":"base","entity_id":"trip-42","event_type":"trip_completed","amount":"100"}])
    out, _ = p.process([{"event_id":"refund","entity_id":"trip-42","event_type":"refund","amount":"-25"}])
    assert out["trip-42"] == Decimal("75")
