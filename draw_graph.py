import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point

def load_nodes(dist_point_data, cabinet_data):
    
    G = nx.Graph()

    for cab in cabinet_data:
        cab_name = [cab['properties']['name']]
        cab_coordinates = cab['geometry']['coordinates']
        G.add_nodes_from(cab_name, pos=cab_coordinates)

        for node in dist_point_data:
            if cab['properties']['name'] == node['properties']['link']:
                node_name = [node['properties']['name']]
                node_coordinates = node['geometry']['coordinates']
                G.add_nodes_from(node_name, pos=node_coordinates)

    for cab in cabinet_data:
        for node in dist_point_data:
            if cab['properties']['name'] == node['properties']['link']:                   
                cab_node_geom = Point(cab['geometry']['coordinates'])
                node_geom = Point(node['geometry']['coordinates'])
                distance = round(cab_node_geom.distance(node_geom),2)
                G.add_edge(cab['properties']['name'],node['properties']['name'],weight=distance)

    return G

from itertools import combinations, chain
from networkx.utils import pairwise, not_implemented_for

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

if __name__ == "__main__":

    GEOJSON_DIST_POINTS = [
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [0.118, 52.204]
            },
            'properties': {
                'name': 'cambridge',
                'link': 'london'
            }
        },
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [-1.286, 51.790]
            },
            'properties': {
                'name': 'oxford',
                'link': 'london'
            }
        },
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [1.257, 52.626]
            },
            'properties': {
                'name': 'norwich',
                'link': 'london'
            }
        },
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [-1.816, 51.070]
            },
            'properties': {
                'name': 'salisbury',
                'link': 'london'
            }
        },
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [-2.575, 51.463]
            },
            'properties': {
                'name': 'bristol',
                'link': 'london'
            }
        }
    ]
    GEOJSON_CABINETS = [
        {
            'type': "Feature",
            'geometry':{
                "type": "Point",
                "coordinates": [-0.129, 51.507]
            },
            'properties': {
                'name': 'london'
            }
        }
    ]



graph = load_nodes(GEOJSON_DIST_POINTS, GEOJSON_CABINETS)

graph2 = steiner_tree(graph, graph.nodes, weight = 'distance') 

plt.figure()
nx.draw_networkx(graph2)
plt.show()
