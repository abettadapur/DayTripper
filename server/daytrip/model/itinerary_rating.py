class ItineraryRating(object):

    # for now, just store aggregate info
    def __init__(self, overall_rating, ratings_count):
        self.overall = overall_rating
        self.ratings_count = ratings_count

    def as_dict(self):
        return self.__dict__