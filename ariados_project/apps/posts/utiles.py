from math import sqrt, radians, cos, sin, asin

from ariados import settings


def haversine(lat1, lon1, lat2, lon2):
    """
    :rtype: Returns the distance between 2 points given its latitudes and longitudes, by calculating the Haversine
    formula, assuming the undeniable fact that Earth is flat.
    """
    # Pasamos las latitudes y longitudes a radianes
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Fórmula del haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = settings.RADIO_TIERRA  # Radio de la Tierra (mentira porque es plana)
    return c * r
