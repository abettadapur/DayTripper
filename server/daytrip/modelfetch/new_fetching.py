from __future__ import division


INFINITY = float("inf")


class Preference:
    """
    Values that fall outside the given range
    are given an error based on how far outside the
    preferred range they are.
    """

    def __init__(self, pref_min, pref_max, abs_min, abs_max):
        self.pref_min = pref_min
        self.pref_max = pref_max
        self.abs_min = abs_min
        self.abs_max = abs_max

    def normalized_error(self, value):
        """If desired, we could 'inject' entropy here?"""
        if self.pref_min <= value <= self.pref_max:
            return 0
        elif value < self.pref_min:
            return (self.pref_min - value) / self.abs_max
        else:
            return (value - self.pref_max) / self.abs_max


class StrictPreference(Preference):
    """
    Values that fall outside the given range are assigned
    a set error value.
    """

    def normalized_error(self, value):
        if self.pref_min <= value <= self.pref_max:
            return 0
        else:
            return 1


def price_preference(pref_min, pref_max):
    return Preference(pref_min, pref_max, 0, 5)


def rating_preference(pref_min, pref_max):
    return Preference(pref_min, pref_max, 0, 5)


def distance_preference(pref_min, pref_max):
    return StrictPreference(pref_min, pref_max, 0, INFINITY)


DEFAULT_PREFERENCES = {
    'price': price_preference(0, 1),
    'rating': rating_preference(4, 5)
    # TODO distance -- need to utilize distance matrix to calculate values
}


class ItemNode:

    def __init__(self, item, neighbors=[], preferences=DEFAULT_PREFERENCES):
        self.item = item
        self.neighbors = []
        self.weights = {}
        self.is_root = False
        self.preferences = preferences

    def refresh_adj_edge_weights(self):
        self.weights.clear()
        for neighbor in self.neighbors:
            self.weights[neighbor] = self.edge_weight(neighbor)

    def edge_weight(self, neighbor):
        # TODO if distance is implemented, ignore that edge_weight
        # calculation if self is the root
        # (because the root does not represent a real item,
        #  so it does not have a location)
        return self.preferences['price'].normalized_error(neighbor.item.yelp_entry.price) \
            + self.preferences['rating'].normalized_error(neighbor.item.yelp_entry.rating)


    @staticmethod
    def single_source_root():
        root = ItemNode(None)
        root.is_root = True
        return root


class DistanceMatrix:
    """Converted algorithm to single-source, so this could be just a list..."""

    def __init__(self, nodes):
        self.nodes = nodes
        self.distances = {}

    def get(self, node_src, node_dest):
        if node_src is node_dest:
            return 0
        elif node_src not in self.distances:
            return INFINITY
        elif node_dest not in self.distances[node_src]:
            return INFINITY
        else:
            return self.distances[node_src][node_dest]

    def put(self, node_src, node_dest, distance):
        if node_src not in self.distances:
            self.distances[node_src] = {node_dest: distance}
        else:
            self.distances[node_src][node_dest] = distance


def ss_shortest_path(source_node, top_sorted_nodes, distance_matrix, predecessor_map):
    for node in top_sorted_nodes:
        for neighbor in node.neighbors:
            print "( " + str(node.item) + ", " + str(neighbor.item) + ")"
            if distance_matrix.get(source_node, neighbor) \
                    > distance_matrix.get(source_node, node) + node.weights[neighbor]:
                distance_matrix.put(
                    source_node,
                    neighbor,
                    distance_matrix.get(source_node, node) + node.weights[neighbor]
                )
                predecessor_map[neighbor] = node


def get_top_sorted_item_nodes(item_candidates_grouped_by_timeslot):
    item_nodes_grouped_by_timeslot = []
    for item_candidates in item_candidates_grouped_by_timeslot:
        node_timeslot_group = []
        for item in item_candidates:
            node_timeslot_group.append(ItemNode(item))
        item_nodes_grouped_by_timeslot.append(node_timeslot_group)

    prev_timeslot_nodes = []

    # traverse backwards to setup edges
    next_timeslot_nodes = []
    for item_nodes in reversed(item_nodes_grouped_by_timeslot):
        for item_node in item_nodes:
            item_node.neighbors = next_timeslot_nodes
        next_timeslot_nodes = item_nodes

    # traverse forwards to get top-sort
    top_sorted_item_nodes = []
    for item_nodes in item_nodes_grouped_by_timeslot:
        for item_node in item_nodes:
            top_sorted_item_nodes.append(item_node)

    return top_sorted_item_nodes


def get_items_for_itinerary(item_candidates_grouped_by_timeslot):
    num_source_candidates = len(item_candidates_grouped_by_timeslot[0])
    num_final_candidates = len(item_candidates_grouped_by_timeslot[-1])

    item_nodes = get_top_sorted_item_nodes(item_candidates_grouped_by_timeslot)

    source_nodes = item_nodes[:num_source_candidates]

    # make a "fake" root node so that we can just run one
    # single-source shortest path
    #
    # "fake", because it represents no true item
    root_node = ItemNode.single_source_root()
    root_node.neighbors = source_nodes
    item_nodes.insert(0, root_node)

    for node in item_nodes:
        node.refresh_adj_edge_weights()

    print [node.item for node in item_nodes]

    distance_matrix = DistanceMatrix(item_nodes)
    predecessor_map = {}
    ss_shortest_path(root_node, item_nodes, distance_matrix, predecessor_map)

    final_nodes = item_nodes[-1*num_final_candidates:]

    # get the shortest valid path
    min_distance = INFINITY
    min_final_node = None
    for final_node in final_nodes:
        if distance_matrix.get(root_node, final_node) < min_distance:
            min_distance = distance_matrix.get(root_node, final_node)
            min_final_node = final_node

    # BEGIN printing
    keys = predecessor_map.keys()
    print [node.item for node in keys]
    print [predecessor_map[key].item for key in keys if key is not None]
    # END printing

    shortest_path = [min_final_node]
    num_timeslots = len(item_candidates_grouped_by_timeslot)
    while len(shortest_path) < num_timeslots:
        predecessor = predecessor_map[shortest_path[0]]
        shortest_path.insert(0, predecessor)

    return [node.item for node in shortest_path]


if __name__ == '__main__':
    groupA = ['itemA', 'itemB', 'itemC']
    groupB = ['item1', 'item2', 'item3']
    groupC = ['item4', 'item5']
    print get_items_for_itinerary([groupA, groupB, groupC])