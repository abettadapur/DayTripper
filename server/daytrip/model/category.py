
class Category(object):

    def __init__(self, name, filters, search_term):
        self.name = name
        self.filters = filters
        self.search_term = search_term

    def as_dict(self):
        return self.__dict__
