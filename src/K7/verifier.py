import numpy as np

#all 21 edges
edges = []

for i in range(1,8):
  for j in range(i+1, 8):
    edges.append((i,j))

#given a vertex i, gives all edges connected to that vertex i
vertex_edges = {}
for i in range(1,8):
  vertex_edges[i] = []

  for edge in edges:
    if i in edge:
      vertex_edges[i].append(edge)

def game_result(a,b):
  #if they return the same edge, they won
  if a == b:
    return 1
  #if they return disjoint edges, they won (this can't happen if Alice and Bob are given the same vertex)
  if a[0] != b[0] and a[0] != b[1]:
    if a[1] != b[0] and a[1] != b[1]:
      return 1

  return 0