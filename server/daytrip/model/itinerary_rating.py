class ItineraryRating(object):

    # for now, just store aggregate info
    def __init__(self, id, itinerary_id, user_id, rating):
        self.id = id
        self.itinerary_id = itinerary_id
        self.user_id = user_id
        self.rating = rating

    def as_dict(self):
        return self.__dict__