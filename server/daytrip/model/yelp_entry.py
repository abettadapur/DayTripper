

class YelpEntry(object):
    def __init__(self, id, name, phone, image_url, url, rating, review_count, location):
        self.id = id
        self.name = name
        self.phone = phone
        self.image_url = image_url;
        self.url = url
        self.rating = rating
        self.location = location
        self.review_count = review_count


    def asDict(self):
        edict = self.__dict__
        edict['location'] = self.location.asDict()
        return edict
