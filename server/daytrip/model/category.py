
class Category(object):

    def __init__(self, name, filters):
        self.name = name
        self.filters = filters

    def as_dict(self):
        return self.__dict__
