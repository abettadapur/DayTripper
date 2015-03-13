import googlemaps
from etc import config


maps = googlemaps.Client(key=config.MAPS_KEY)


def travel_time_matrix(origin, destinations):
	distance_data = maps.distance_matrix(origin, destinations);
	return distance_data;

def directions(origin, destination):
	directions = maps.directions(origin, destination)
	return directions

