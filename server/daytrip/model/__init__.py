from model.category import Category
categories = []
categories.append(Category('breakfast', ['breakfast_brunch'], ''))
categories.append(Category('lunch', ['restaurants'], 'lunch'))
categories.append(Category('dinner', ['restaurants'], 'dinner'))
categories.append(Category('attraction', ['active','parks','shopping'],'fun'))
categories.append(Category('nightlife', ['bars','beergardens','comedyclubs','jazzandblues','karaoke','poolhalls'],''))

def match_category(category_name):
    for c in categories:
        if c.name==category_name:
            return c

    return None


def category_default_duration(category_name, default=60):
    """Returns number of minutes"""
    if category_name in ['breakfast']:
        return 45
    elif category_name in ['lunch', 'dinner', 'attraction']:
        return 60
    elif category_name in ['nightlife']:
        return 100
    else:
        return default
