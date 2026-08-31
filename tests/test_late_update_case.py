from decimal import Decimal
from platform_core.pipeline import TripCollectionPipeline

def test_old_event_time_new_commit_semantics_at_domain_boundary():
    p = TripCollectionPipeline()
    p.process([{"event_id":"base-42","entity_id":"trip-42","event_type":"trip_completed","amount":"100","event_time":"2020-01-01"}])
    out, _ = p.process([{"event_id":"refund-42","entity_id":"trip-42","event_type":"refund","amount":"-25","event_time":"2020-01-02"}])
    assert out["trip-42"] == Decimal("75")
