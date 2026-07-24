import numpy as np
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit.providers.basic_provider import BasicSimulator
import random

from src.K7.bases import bases
from src.K7.verifier import vertex_edges, game_result
from src.K7.quantumcircuit import game_circuit


#random edge chosen

#a, b are the chosen vertices for alice and bob
#x, y, are the two vertices that are removed
#n is an odd integer greater than or equal to 9 equal to the number of total vertices in the graph
def strategy(a,b,x,y,n):
    #define the dictionary so that the function works
    local_to_actual = {}
    
    #game_circuit returns a pair and we want a integer
    def e(e):
        return (local_to_actual[e[0]], local_to_actual[e[1]])

    k7 = []

    #generates k7 that includes one vertex of the removed edge
    for i in range (x,n+1):
        if i != y and len(k7)<7:
           k7.append(i)
    if len(k7)<7:
       for i in range(1,x):
          if i != y and len(k7)<7:
             k7.append(i)


    #generates a list of all other vertices not used in k7
    other_vertices = []
    for i in range(1,n+1):
       if i not in k7:
          other_vertices.append(i)


    #pairs all of the non-used vertices up
    paired_edges = []
    for i in range(0, len(other_vertices),2):
       paired_edges.append((other_vertices[i], other_vertices[i+1]))


    #if alice/bob's vertice is not in the K7, then defaults to the paired edge associated with that vector
    def find_edge(v):
       for i in paired_edges:
          if v in i:
             return i

    #same logic as K9quantumcircuit.py
    actual_to_local = {k7[0]:1, k7[1]:2, k7[2]:3, k7[3]:4, k7[4]:5, k7[5]:6, k7[6]:7}
    local_to_actual = {1:k7[0], 2:k7[1], 3:k7[2], 4:k7[3], 5:k7[4], 6:k7[5], 7:k7[6]}
    
    
    #same logic as K9quantumcircuit.py
    if a in k7 and b in k7:
        local_a, local_b = game_circuit(actual_to_local[a],actual_to_local[b])
        return e(local_a), e(local_b)
          
    elif a in k7:
        local_a, local_b = game_circuit(actual_to_local[a],1)
        

        
        return e(local_a), find_edge(b)
          
    elif b in k7:
        local_a, local_b = game_circuit(1,actual_to_local[b])
        return find_edge(a), e(local_b)
    else:
        return find_edge(a), find_edge(b)




total = 0
for alice_vertex in range(1, 14):
    for bob_vertex in range(1, 14):   
      alice_edge, bob_edge = strategy(alice_vertex, bob_vertex, 5,8, 13)
      total = total + game_result(alice_edge, bob_edge)

print(total)

