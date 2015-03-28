import itinerary
import users


ITINERARY_ID = 'itinerary_id'
USER_ID = 'user_id'
RATING = 'rating'

ITINERARY_RATING_TABLE = 'itinerary_rating'

CREATE_ITINERARY_RATING_TABLE = '''
create table if not exists {table} (
    {itinerary_id} integer not null,
    {user_id} integer not null,
    {rating} integer,
    primary key({itinerary_id}, {user_id}),
    foreign key({itinerary_id}) references {itinerary_table}({itinerary_table_id}),
    foreign key({user_id}) references {user_table}({user_table_id})
)
'''.format(
    table=ITINERARY_RATING_TABLE,
    itinerary_id=ITINERARY_ID,
    user_id=USER_ID,
    rating=RATING,
    itinerary_table=itinerary.ITINERARY_TABLE,
    itinerary_table_id=itinerary.ID,
    user_table=users.USERS_TABLE,
    user_table_id=users.ID
)
