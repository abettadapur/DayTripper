__author__ = 'abettadapur'


class User(object):

    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def as_dict(self):
        return self.__dict__