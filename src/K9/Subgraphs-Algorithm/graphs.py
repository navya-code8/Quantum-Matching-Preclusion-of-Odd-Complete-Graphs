import numpy as np

#we want to generate the graphs that the algorithm will be looping
#first, define all the vertices:
vertices = [0,1,2,3,4,5,6,7,8]

#given two vertices, we can make an edge.
def edge(u,v):
    return tuple[(u,v)] if u < v else tuple[(v,u)]

#the complete graph K9
K9_edges = []
for u in vertices:
    for v in vertices:
        if u <v:
            K9_edges.append((u,v))

#we want subgraphs
def subgraph(deleted_edges):
    deleted = []
    for u,v in deleted_edges:
        deleted.append(edge(u,v))

    subgraph = []

    #generate the edges without the deleted ones
    for edges in K9_edges:
        if edges not in deleted:
            subgraph.append(edges)
    return subgraph

#we also define a function which returns all edges incident to a vertex.
def incident_edges(vertex, graph_edges):
    current_edge = []

    for i in graph_edges:
        if vertex in i:
            current_edge.append(i)

    return current_edge

#we also define a function which returns all vertices incident to a vertex.
def incident_vertices(vertex, graph_edges):
    vertices = []

    #for all edges that include a vertex, add the other vertex to the list.
    for u,v in incident_edges(vertex, graph_edges):
        if u == vertex:
            vertices.append(v)
        else:
            vertices.append(u)

    return vertices
