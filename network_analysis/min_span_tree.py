# https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
# Python program for Kruskal's algorithm to find 
# Minimum Spanning Tree of a given connected, 
# undirected and weighted graph 
# by Neelam Yadav 

from collections import defaultdict 
from shapely.geometry import shape
import pprint

#Class to represent a graph 
class Graph: 

    def __init__(self,vertices): 
        self.V= vertices #No. of vertices
        self.graph = [] # default dictionary 
        # to store graph 

	# function to add an edge to graph 
    def addEdge(self,u,v,w): 
    	self.graph.append([u,v,w]) 

    def find_unique_edges(self):
        my_graph = self.graph
        unique_graph = []

        for l in my_graph:
            # print('l is unsorted {}'.format(l))
            weight = l[2]
            nodes = l[:2]
            # print('nodes are {}'.format(nodes))
            nodes = sorted(nodes)
            # print('sorted nodes are {}'.format(nodes))
            nodes.append(weight)
            # print('all sorted nodes are {}'.format(nodes))
            unique_graph.append(nodes)
            # print('l is sorted {}'.format(nodes))

        unique_graph = list(set(tuple(i) for i in unique_graph))

        self.graph = [] 
        for u, v, w in unique_graph:
            # print(u, v, w)
            self.graph.append([u,v,w]) 

		
		
	# A utility function to find set of an element i 
	# (uses path compression technique) 
    def find(self, parent, i): 
        print('find for {} is {}'.format(parent, i))
        #catch = parent[i]
        #print('parent[i] is {}'.format(catch))
        if parent[i] == i: 
            return i, print('returned (if) {}'.format(i)) 
        return self.find(parent, parent[i]), print('returned self.find({}, {})'.format(parent, parent[i]))  

	# A function that does union of two sets of x and y 
	# (uses union by rank) 
    def union(self, parent, rank, x, y): 
    	xroot = self.find(parent, x) 
    	yroot = self.find(parent, y) 
    	print('xroot is {}'.format(x))
    	print('yroot is {}'.format(y))
		# Attach smaller rank tree under root of 
		# high rank tree (Union by Rank) 
    	if rank[xroot] < rank[yroot]: 
    		parent[xroot] = yroot 
    	elif rank[xroot] > rank[yroot]: 
    		parent[yroot] = xroot 

		# If ranks are same, then make one as root 
		# and increment its rank by one 
    	else : 
    		parent[yroot] = xroot 
    		rank[xroot] += 1

    # The main function to construct MST using Kruskal's algorithm 
    def KruskalMST(self):
        
        result =[] #This will store the resultant MST 
        
        i = 0 # An index variable, used for sorted edges 
        e = 0 # An index variable, used for result[] 

            # Step 1: Sort all the edges in non-decreasing 
                # order of their 
                # weight. If we are not allowed to change the 
                # given graph, we can create a copy of graph 
        # pprint.pprint(self.graph)
        self.graph = sorted(self.graph,key=lambda item: item[2]) 
        print('sorted_graph')
        pprint.pprint(self.graph)
        # print('sorted_graph')
        parent = [] ; rank = [] 
        
        vertices = self.V

        print('vertices count is {}'.format(vertices))

        # Create V subsets with single elements 
        for node in range(self.V): 
            parent.append(node) 
            rank.append(0) 
        pprint.pprint('parent is {}'.format(parent))

        # Number of edges to be taken is equal to V-1 
        while e < self.V -1 : 
            print('i is {}'.format(i))
            #print(i)
            # Step 2: Pick the smallest edge and increment 
                    # the index for next iteration 
            print(self.graph[i])
            u,v,w = self.graph[i]
            print('u is {}'.format(u))
            print('v is {}'.format(v))
            print('w is {}'.format(w))

            print('i is {}'.format(i))

            i = i + 1
            x = self.find(parent, u) 
            y = self.find(parent, v) 

            print('x is {}'.format(x))
            print('y is {}'.format(y))
            # If including this edge does't cause cycle, 
                        # include it in result and increment the index 
                        # of result for next edge 
            if x != y: 
                print('x not equal to y')
                e = e + 1	
                result.append([u,v,w]) 
                print('x is {}'.format(x))
                print('y is {}'.format(y))
                self.union(parent, rank, x, y)			 
            # Else discard the edge 

        # print the contents of result[] to display the built MST 
        print ("Following are the edges in the constructed MST")
        for u,v,weight in result: 
            #print str(u) + " -- " + str(v) + " == " + str(weight) 
            print ("%d -- %d == %d" % (u,v,weight)) 
    
        return result


def load_nodes(nodes):
    
    graph_size = len(nodes) #* len(nodes)

    print('length is {}'.format(graph_size))

    G = Graph(graph_size)

    for node1 in nodes:
        for node2 in nodes:
            if node1['properties']['id'] != node2['properties']['id']: 
                
                node1_id = node1['properties']['id']
                node1_geom = shape(node1['geometry'])
                
                node2_id = node2['properties']['id']
                node2_geom = shape(node2['geometry'])

                distance_weight = round(node1_geom.distance(node2_geom), 4)
                
                G.addEdge(node1_id, node2_id, distance_weight)

    G.find_unique_edges()

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
  
#Driver code 
g = Graph(4) 
g.addEdge(0, 1, 10) 
g.addEdge(0, 2, 6) 
g.addEdge(0, 3, 5) 
g.addEdge(1, 3, 15) 
g.addEdge(2, 3, 4) 
#print(g.graph)
test = g.KruskalMST()
# print(test)

# network = load_nodes(GEOJSON_DIST_POINTS)

# #test = network.find_unique_edges()

# pprint.pprint(network.graph)

# mst = network.KruskalMST() 

# # pprint.pprint(mst)
