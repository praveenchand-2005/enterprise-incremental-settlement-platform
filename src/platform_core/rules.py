from decimal import Decimal

def base_fare_rule(trip):
    return trip.base_fare

def tip_rule(trip):
    return trip.tip_total

def refund_rule(trip):
    return -trip.refund_total

def settlement_total(trip):
    return base_fare_rule(trip) + tip_rule(trip) + refund_rule(trip)
