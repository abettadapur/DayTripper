class YelpLocation(object):

    def __init__(self, yelp_id, address, city, zip_code, state, latitude, longitude):
        self.yelp_id = yelp_id
        self.address = address
        self.city = city
        self.postal_code = zip_code
        self.state_code = state
        self.latitude = latitude
        self.longitude = longitude


    def as_dict(self):
        loc_dict = self.__dict__
        loc_dict['coordinate'] = {'latitude': self.latitude, 'longitude': self.longitude}
        del loc_dict['latitude']
        del loc_dict['longitude']
        return loc_dict
