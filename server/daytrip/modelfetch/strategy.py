import random
import db


def run_strategy(strategy_name, yelp_ids):
    """
    Returns index of selected yelp_id, or -1 if strategy failed.

    Defaults to RANDOM strategy on invalid strategy_name.
    """
    if strategy_name not in STRATEGIES:
        strategy_name = "random"
    return STRATEGIES[strategy_name](yelp_ids)


def strategy_price_for(price_limit):
    return lambda yelp_ids: find_first_not_exceeding(yelp_ids, price_limit)


def find_first_not_exceeding(yelp_ids, price_limit):
    for index, yelp_id in enumerate(yelp_ids):
        yelp_entry = db.sqlite.get_yelp_entry(yelp_id)
        if yelp_entry.price is not None\
                and yelp_entry.price <= price_limit:
            return index
    return -1


def strategy_random(yelp_ids):
    return random.randrange(len(yelp_ids))


def strategy_popularity(yelp_ids):
    counts = [db.sqlite.get_yelp_count_in_items(yelp_id)
              for yelp_id in yelp_ids]
    max_index = counts.index(max(counts))
    return max_index


def strategy_first(yelp_ids):
    return 0


# A strategy accepts yelp_ids as input,
# and returns a selected index as output (or -1 on a failure)
#
# Two special strategies not included in this module:
#   distance:     utilizes maps module
#   yelp-rating:  utilizes yelp api search parameter
STRATEGIES = {
    "price-0": strategy_price_for(0),
    "price-1": strategy_price_for(1),
    "price-2": strategy_price_for(2),
    "price-3": strategy_price_for(3),
    "price-4": strategy_price_for(4),
    "random": strategy_random,
    "popularity": strategy_popularity,
    "first": strategy_first
}