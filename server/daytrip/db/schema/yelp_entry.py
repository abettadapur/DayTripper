ID = 'id'
PHONE = 'phone'
IMAGE_URL = 'image_url'
URL = 'url'
NAME = 'name'
RATING = 'rating'

YELP_ENTRY_TABLE = 'yelp_entries'

CREATE_YELP_ENTRY_TABLE = '''create table if not exists {0}
({1} text primary key, {2} text, {3} text, {4} text, {5} text, {6} integer);
'''.format(YELP_ENTRY_TABLE, ID, PHONE, IMAGE_URL, URL, NAME, RATING)
