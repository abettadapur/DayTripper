__author__ = 'abettadapur'

class Itinerary(object):

    def __init__(self, id, user, name, date, start_time, end_time, city, items):
        self.id = id
        self.user = user
        self.name = name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.city = city
        self.items = items