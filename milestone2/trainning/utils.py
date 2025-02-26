from math import radians, sin, cos, atan2, sqrt


def earth_distance(x, y):
    # Approximate radius of earth in km
    R = 6373.0

    lat1, lng1 = radians(x[0]), radians(x[1])
    lat2, lng2 = radians(y[0]), radians(y[1])

    dlon = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c * 1000
