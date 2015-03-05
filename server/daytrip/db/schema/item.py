import itinerary

ID = 'id'
ITINERARY_ID = 'itinerary_id'
YELP_ID = 'yelp_id'
CATEGORY = 'category'
NAME = 'name'
START_TIME = 'start_time'
END_TIME = 'end_time'

ITEM_TABLE = 'items'

CREATE_ITEM_TABLE = '''create table if not exists {0}
({1} integer primary key autoincrement, {2} integer, {3} integer, {4} text, {5} text, {6} integer, {7} integer, foreign key({2}) references {8}({9}));
'''.format(ITEM_TABLE, ID, ITINERARY_ID, YELP_ID, CATEGORY, NAME, START_TIME, END_TIME, itinerary.ITINERARY_TABLE, itinerary.ID)

