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


    def as_dict(self):
        idict = self.__dict__
        idict['user'] = self.user.as_dict()
        for i in range(0,len(idict['items'])):
            idict['items'][i] = idict['items'][i].as_dict()

        return idict