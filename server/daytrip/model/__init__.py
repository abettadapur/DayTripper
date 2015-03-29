from model.category import Category
categories = []
categories.append(Category('breakfast', ['breakfast_brunch'], ''))
categories.append(Category('lunch', ['restaurants'], 'lunch'))
categories.append(Category('dinner', ['restaurants'], 'dinner'))
categories.append(Category('attraction', ['active','arts','parks','shopping'],'fun'))
categories.append(Category('nightlife', ['bars','beergardens','comedyclubs','jazzandblues','karaoke','poolhalls'],''))

def match_category(category_name):
    for c in categories:
        if c.name==category_name:
            return c

    return None
