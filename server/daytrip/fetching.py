from model.itinerary import Itinerary
from model.item import Item
from yelp import yelpapi

import model
import db
import random
import dateutil.parser
import datetime


BREAKFAST = 'breakfast'
LUNCH = 'lunch'
ATTRACTION = 'attraction'
DINNER = 'dinner'
NIGHTLIFE = 'nightlife'

DEFAULT_SCHEDULE = [
    BREAKFAST,
    LUNCH,
    ATTRACTION,
    DINNER,
    NIGHTLIFE
]

# ranges (inclusive) are non-overlapping to simplify sample generation
CATEGORY_START_HOURS = {
    BREAKFAST: (8, 10),
    LUNCH: (12, 13),
    ATTRACTION: (14, 17),
    DINNER: (18, 20),
    NIGHTLIFE: (21, 22)
}

CATEGORIES = [model.match_category(name) for name in DEFAULT_SCHEDULE]


def fetch_sample_itinerary(user, name, city, start_time, end_time, date):
    """
    start_time, end_time, and date should be STRINGS straight from args[]
    (i.e. don't pass datetime object result of dateutil.parser.parse)

    Does not persist itinerary to DB!
    """
    valid_categories = filter_valid_categories(CATEGORIES, start_time, end_time)
    sample_items = fetch_sample_items(city, valid_categories)
    update_start_end_times(sample_items, start_time)

    sample_itinerary = Itinerary(
        id=None,
        user=user,
        name=name,
        date=date,
        start_time=start_time,
        end_time=end_time,
        city=city,
        items=sample_items
    )

    return sample_itinerary


def filter_valid_categories(categories, start_time, end_time):
    results = []

    start_hour = dateutil.parser.parse(start_time).hour
    end_hour = dateutil.parser.parse(end_time).hour

    for category in categories:
        start_min, start_max = CATEGORY_START_HOURS[category.name]
        if start_hour <= start_max and end_hour >= start_min:
            results.append(category)

    return results


def fetch_sample_items(city, categories):
    """ Does not set start/end times """
    sample_items = []
    used_yelp_ids = []

    search_location = city
    coordinate_str = None
    for category in categories:
        new_item = fetch_new_item(search_location, category, coordinate_str=coordinate_str, disallowed_yelp_ids=used_yelp_ids)
        sample_items.append(new_item)

        used_yelp_ids.append(new_item.yelp_id)
        search_location = new_item.yelp_entry.location.city
        coordinate_str = new_item.yelp_entry.location.coordinate_string()

    return sample_items



def fetch_new_item(location, category, start_time="", end_time="", coordinate_str=None, disallowed_yelp_ids=[]):
    """
    If start_time, end_time not specified, callee must add these to Item!

    coordinate_str is for 'cll' param in yelp search query string

    Does not persist Item result to the database!
    """
    yelp_id, item_name = best_yelp_id_with_name(location, category, coordinate_str=coordinate_str, disallowed_yelp_ids=disallowed_yelp_ids)

    item = Item(
        id=None,
        yelp_id=yelp_id,
        category=category.name,
        name=item_name,
        start_time=start_time,
        end_time=end_time
    )
    item.yelp_entry = db.sqlite.get_yelp_entry(yelp_id)
    return item


def best_yelp_id_with_name(location, category, coordinate_str=None, disallowed_yelp_ids=[]):
    """coordinate_str is for cll param in query string"""
    if coordinate_str is not None:
        search_results = yelpapi.search(category.search_term, location, category.filters, cll=coordinate_str)
    else:  # location is city
        search_results = yelpapi.search(category.search_term, location, category.filters)

    candidate_ids_with_names = [(result['id'], result['name'])
                                for result
                                in search_results
                                if result['id'] not in disallowed_yelp_ids]

    if len(candidate_ids_with_names) == 0:
        print "best_yelp_id_with_name: no good ids found!  returning random result"
        default_result = search_results[random.randrange(len(search_results))]
        return default_result['id'], default_result['name']

    # TODO create multiple "strategies" for selecting the result
    index = 0
    yelp_id = candidate_ids_with_names[index][0]
    yelp_name = candidate_ids_with_names[index][1]
    return yelp_id, yelp_name


def update_start_end_times(items, start_time, min_gap_minutes=15):
    """"Intended to be used only for initial itinerary generation"""
    next_valid_start_time = start_time
    for item in items:
        # prevent issues like BREAKFAST ends as 10AM, LUNCH starts at 10:15AM
        default_category_start_hour = CATEGORY_START_HOURS[item.category][0]
        default_category_start_time = new_timestr_with_hour(start_time, default_category_start_hour)

        item.start_time = max_timestr(next_valid_start_time, default_category_start_time)
        item.end_time = add_minutes(item.start_time,
                                    model.category_default_duration(item.category))

        next_valid_start_time = add_minutes(item.end_time, min_gap_minutes)


def new_timestr_with_hour(ref_timestr, new_hours):
    dtime = dateutil.parser.parse(ref_timestr)
    new_dtime = dtime.replace(hour=new_hours)
    new_timestr = new_dtime.isoformat()
    return new_timestr


def add_minutes(timestr, minutes):
    dtime = dateutil.parser.parse(timestr)
    new_dtime = dtime + datetime.timedelta(minutes=minutes)
    new_timestr = str(new_dtime.isoformat())
    return new_timestr


def max_timestr(timestr1, timestr2):
    dtime1 = dateutil.parser.parse(timestr1)
    dtime2 = dateutil.parser.parse(timestr2)
    if dtime1 > dtime2:
        return timestr1
    else:
        return timestr2