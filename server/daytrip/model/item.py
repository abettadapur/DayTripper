class Item(object):
    def __init__(self, id, yelp_id, category, name, start_time, end_time):
        self.id = id
        self.yelp_id = yelp_id
        self.category = category
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.yelp_entry = None

    def as_dict(self):
        idict = self.__dict__
        if self.yelp_entry:
            idict['yelp_entry'] = self.yelp_entry.asDict()
        return idict
