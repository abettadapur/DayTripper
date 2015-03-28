ID = 'id'
PHONE = 'phone'
IMAGE_URL = 'image_url'
URL = 'url'
NAME = 'name'
RATING = 'rating'
REVIEW_COUNT = 'review_count'
PRICE = 'price'

YELP_ENTRY_TABLE = 'yelp_entries'

CREATE_YELP_ENTRY_TABLE = '''create table if not exists {0}
({1} text primary key, {2} text, {3} text, {4} text, {5} text, {6} integer, {7} integer, {8} integer);
'''.format(YELP_ENTRY_TABLE, ID, PHONE, IMAGE_URL, URL, NAME, RATING, REVIEW_COUNT, PRICE)
