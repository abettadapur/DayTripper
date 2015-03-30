import googlemaps
from etc import config


maps = googlemaps.Client(key=config.MAPS_KEY)


def travel_time_matrix(origin, destinations):
    distance_data = maps.distance_matrix(origin, destinations)
    return distance_data


def closest_item(origin, destinations):
    distance_data = travel_time_matrix(origin, destinations)
    elements = distance_data['rows'][0]['elements']
    min_time = elements[0]['duration']['value']
    min_index = 0
    for i in range(0, len(elements)):
        try:
            if elements[i]['duration']['value'] < min_time:
                print elements[i]
                min_index = i
        except KeyError as kex:
            pass

    return min_index


def directions(origin, destination):
    directions = maps.directions(origin, destination)
    return directions
