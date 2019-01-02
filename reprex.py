import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point
from itertools import combinations, chain
from networkx.utils import pairwise, not_implemented_for


def load_nodes(premises_data, distribution_point_data):

    G = nx.Graph()

    for dist_point in distribution_point_data:
        dist_point_name = [dist_point['properties']['name']]
        dist_point_coordinates = dist_point['geometry']['coordinates']
        G.add_nodes_from(dist_point_name , pos=dist_point_coordinates )

        for premises in premises_data:
            if dist_point['properties']['name'] == premises ['properties']['link']:
                premises_name = [premises ['properties']['name']]
                premises_coordinates = premises['geometry']['coordinates']
                G.add_nodes_from(premises_name, pos=premises_coordinates )

    for dist_point in distribution_point_data:
        for premises in premises_data:
            if dist_point['properties']['name'] == premises['properties']['link']:                   
                dist_point_geom = Point(dist_point['geometry']['coordinates'])
                premises_geom = Point(premises['geometry']['coordinates'])
                distance = round(dist_point_geom.distance(premises_geom),2)
                G.add_edge(dist_point['properties']['name'],premises['properties']['name'],weight=distance)

    return G


def metric_closure(G, weight='weight'):
    """  Return the metric closure of a graph.

    The metric closure of a graph *G* is the complete graph in which each edge
    is weighted by the shortest path distance between the nodes in *G* .

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    NetworkX graph
        Metric closure of the graph `G`.

    """
    M = nx.Graph()

    Gnodes = set(G)

    # check for connected graph while processing first node
    all_paths_iter = nx.all_pairs_dijkstra(G, weight=weight)
    u, (distance, path) = next(all_paths_iter)
    if Gnodes - set(distance):
        msg = "G is not a connected graph. metric_closure is not defined."
        raise nx.NetworkXError(msg)
    Gnodes.remove(u)
    for v in Gnodes:
        M.add_edge(u, v, distance=distance[v], path=path[v])

    # first node done -- now process the rest
    for u, (distance, path) in all_paths_iter:
        Gnodes.remove(u)
        for v in Gnodes:
            M.add_edge(u, v, distance=distance[v], path=path[v])

    return M

def steiner_tree(G, terminal_nodes, weight='weight'):
    """ Return an approximation to the minimum Steiner tree of a graph.

    Parameters
    ----------
    G : NetworkX graph

    terminal_nodes : list
            A list of terminal nodes for which minimum steiner tree is
            to be found.

    Returns
    -------
    NetworkX graph
        Approximation to the minimum steiner tree of `G` induced by
        `terminal_nodes` .

    Notes
    -----
    Steiner tree can be approximated by computing the minimum spanning
    tree of the subgraph of the metric closure of the graph induced by the
    terminal nodes, where the metric closure of *G* is the complete graph in
    which each edge is weighted by the shortest path distance between the
    nodes in *G* .
    This algorithm produces a tree whose weight is within a (2 - (2 / t))
    factor of the weight of the optimal Steiner tree where *t* is number of
    terminal nodes.

    """
    # M is the subgraph of the metric closure induced by the terminal nodes of
    # G.
    M = metric_closure(G, weight=weight)
    # Use the 'distance' attribute of each edge provided by the metric closure
    # graph.
    H = M.subgraph(terminal_nodes)
    mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
    # Create an iterator over each edge in each shortest path; repeats are okay
    edges = chain.from_iterable(pairwise(d['path']) for u, v, d in mst_edges)
    T = G.edge_subgraph(edges)
    return T

GEOJSON_PREMISES = [
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [0.129960,52.220977]
            },
            'properties': {
                'name': 'premises_1',
                'link': 'distribution_point'
            }
        },
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [0.130056,52.220895]
            },
            'properties': {
                'name': 'premises_2',
                'link': 'distribution_point'
            }
        },
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [0.130318,52.220782]
            },
            'properties': {
                'name': 'premises_3',
                'link': 'distribution_point'
            }
        },
    ]

GEOJSON_DISTRIBUTION_POINT = [
    {
        'type': "Feature",
        'geometry':{
            "type": "Point",
            "coordinates": [0.129829,52.220802]
        },
        'properties': {
            'name': 'distribution_point'
        }
    }
]

graph = load_nodes(GEOJSON_PREMISES, GEOJSON_DISTRIBUTION_POINT)
graph2 = steiner_tree(graph, graph.nodes, weight = 'weight') 

plt.figure()
nx.draw_networkx(graph2)
plt.show()

