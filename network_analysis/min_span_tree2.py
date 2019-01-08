# https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
# Python program for Kruskal's algorithm to find 
# Minimum Spanning Tree of a given connected, 
# undirected and weighted graph 
# by Neelam Yadav 

from collections import defaultdict 
from shapely.geometry import shape
import pprint


class Graph(object):
    def __init__(self):
        self.g = {}

    def add(self, vertex1, vertex2, weight):
        if vertex1 not in self.g:
            self.g[vertex1] = {}

        if vertex2 not in self.g:
            self.g[vertex2] = {}

        self.g[vertex1][vertex2] = weight
        self.g[vertex2][vertex1] = weight

    def has_link(self, v1, v2):
        return v2 in self[v1] or v1 in self[v2]

    def edges(self):
        data = []

        for from_vertex, destinations in self.g.items():
            for to_vertex, weight in destinations.items():
                if (to_vertex, from_vertex, weight) not in data:
                    data.append((from_vertex, to_vertex, weight))

        return data

    def sorted_by_weight(self, desc=False):
        return sorted(self.edges(), key=lambda x: x[2], reverse=desc)

    def spanning_tree(self, minimum=True):
        mst = Graph()
        parent = {}
        rank = {}

        def find_parent(vertex):
            while parent[vertex] != vertex:
                vertex = parent[vertex]

            return vertex

        def union(root1, root2):
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root2] = root1

                if rank[root2] == rank[root1]:
                    rank[root2] += 1

        for vertex in self.g:
            parent[vertex] = vertex
            rank[vertex] = 0

        for v1, v2, weight in self.sorted_by_weight(not minimum):
            parent1 = find_parent(v1)
            parent2 = find_parent(v2)

            if parent1 != parent2:
                mst.add(v1, v2, weight)
                union(parent1, parent2)

            if len(self) == len(mst):
                break

        return mst

    def __len__(self):
        return len(self.g.keys())

    def __getitem__(self, node):
        return self.g[node]

    def __iter__(self):
        for edge in self.edges():
            yield edge

    def __str__(self):
        return "\n".join('from %s to %s: %d' % edge for edge in self.edges())

def load_nodes(nodes):
    
    G = Graph()

    for node1 in nodes:
        for node2 in nodes:
            if node1['properties']['id'] != node2['properties']['id']: 
                
                node1_id = node1['properties']['id']
                node1_geom = shape(node1['geometry'])
                
                node2_id = node2['properties']['id']
                node2_geom = shape(node2['geometry'])

                distance_weight = round(node1_geom.distance(node2_geom), 4)
                
                G.add(node1_id, node2_id, distance_weight)

    return G

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
                'id': 0,
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
                'id': 1,
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
                'id': 2,
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
                'id': 3,
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
                'id': 4,
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

graph = load_nodes(GEOJSON_DIST_POINTS)

mst = graph.spanning_tree()
# print()
# print(graph.spanning_tree(False))


import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1], weight = edge[2])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos)
    # show graph
    plt.show()

# graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
#          (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

# # you may name your edge labels
# labels = map(chr, range(65, 65+len(graph)))
# #draw_graph(graph, labels)

# if edge labels is not specified, numeric labels (0, 1, 2...) will be used
draw_graph(mst)









