class Item(object):
    def __init__(self, id, yelp_id, category, name, start_time, end_time):
        self.id = id
        self.name = name
        self.category = category
        self.start_time = start_time
        self.end_time = end_time

