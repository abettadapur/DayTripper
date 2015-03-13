YELP_ID = 'yelp_id'
ADDRESS = 'address'
CITY = 'city'
ZIP = 'zip'
STATE = 'state'
LATITUDE = 'latitude'
LONGITUDE = 'longitude'

YELP_LOCATION_TABLE = 'yelp_locations'

CREATE_YELP_LOCATION_TABLE = '''create table if not exists {0}
({1} text, {2} text, {3} text, {4} integer, {5} text, {6} float, {7} float);
'''.format(YELP_LOCATION_TABLE, YELP_ID, ADDRESS, CITY, ZIP, STATE, LATITUDE, LONGITUDE)
