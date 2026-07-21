import random
from datetime import datetime, timedelta

# Small pool of US hub airports used to synthesise routes.
AIRPORTS = [
    ("JFK", "New York"),
    ("LAX", "Los Angeles"),
    ("ORD", "Chicago"),
    ("ATL", "Atlanta"),
    ("DFW", "Dallas"),
    ("SFO", "San Francisco"),
    ("SEA", "Seattle"),
    ("DEN", "Denver"),
    ("BOS", "Boston"),
    ("MIA", "Miami"),
]

FLIGHT_STATUSES = ["ON_TIME", "DELAYED", "CANCELLED"]
# Weighted toward ON_TIME so the data feels plausibly real.
FLIGHT_STATUS_WEIGHTS = [85, 12, 3]


def get_random_int(min_val, max_val):
    """Returns a random int between min_val and max_val, inclusive."""
    return random.randint(min_val, max_val)


def generate_flight(airline):
    """Generate one synthetic flight record with origin/destination + timing."""
    origin, destination = random.sample(AIRPORTS, 2)
    departure = datetime.utcnow() + timedelta(hours=random.randint(1, 48))
    duration_minutes = random.randint(60, 360)
    arrival = departure + timedelta(minutes=duration_minutes)
    return {
        "flight_number": f"{airline}{get_random_int(100, 999)}",
        "airline_code": airline,
        "origin": {"airport_code": origin[0], "city": origin[1]},
        "destination": {"airport_code": destination[0], "city": destination[1]},
        "departure_time": departure.isoformat() + "Z",
        "arrival_time": arrival.isoformat() + "Z",
        "duration_minutes": duration_minutes,
        "status": random.choices(FLIGHT_STATUSES, weights=FLIGHT_STATUS_WEIGHTS)[0],
    }
