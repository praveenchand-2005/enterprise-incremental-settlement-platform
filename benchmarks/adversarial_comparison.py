from decimal import Decimal
from platform_core.pipeline import TripCollectionPipeline

def build_initial(n=1000):
    return [{"event_id":f"base-{i}","entity_id":f"trip-{i}","event_type":"trip_completed","event_version":1,"event_time":"2020-01-01","amount":"100"} for i in range(n)]

def run():
    initial = build_initial()
    fixed = TripCollectionPipeline(); fixed.process(initial); fixed_out,_ = fixed.process([])
    changed = TripCollectionPipeline(); changed.process(initial); changed_out,_ = changed.process([{"event_id":"late-refund-42","entity_id":"trip-42","event_type":"refund","event_version":2,"event_time":"2020-01-02","amount":"-25"}])
    fixed_value = fixed_out.get("trip-42", Decimal("100")); changed_value = changed_out["trip-42"]
    result = {"fixed_window":str(fixed_value),"change_driven":str(changed_value),"expected":"75"}
    print(result)
    assert fixed_value != Decimal("75") and changed_value == Decimal("75")

if __name__ == "__main__": run()
